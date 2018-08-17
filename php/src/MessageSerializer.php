<?php

class MessageSerializer
{
    const MAGIC_BYTE = 0;

    private $idToDecoderFunc = [];
    private $subjectVersionToDecoderFunc = [];

    /** @var AvroIODatumWriter[] */
    private $idToWriters = [];

    /** @var AvroIODatumWriter[][] */
    private $subjectVersionToWriters = [];

    /** @var CachedSchemaRegistryClient */
    private $registry;

    private $registerMissingSchemas = false;

    public function __construct(CachedSchemaRegistryClient $registry, $options = [])
    {
        $this->registry = $registry;

        if (isset($options['register_missing_schemas'])) {
            $this->registerMissingSchemas = $options['register_missing_schemas'];
        }
    }

    /**
     * Encode a record with a given schema id.
     *
     * @param int $schemaId
     * @param array $record A data to serialize
     * @param bool $isKey If the record is a key
     *
     * @return AvroIODatumWriter encoder object
     */
    public function encodeRecordWithSchemaId($schemaId, array $record, $isKey = false)
    {
        if (! isset($this->idToWriters[$schemaId])) {
            $schema = $this->registry->getById($schemaId);

            $this->idToWriters[$schemaId] = new AvroIODatumWriter($schema);
        }

        $writer = $this->idToWriters[$schemaId];

        $io = new AvroStringIO();

        // write the header

        // magic byte
        $io->write(pack('C', static::MAGIC_BYTE));

        // write the schema ID in network byte order (big end)
        $io->write(pack('N', $schemaId));

        // write the record to the rest of it
        // Create an encoder that we'll write to
        $encoder = new AvroIOBinaryEncoder($io);

        // write the object in 'obj' as Avro to the fake file...
        $writer->write($record, $encoder);

        return $io->string();
    }

    /**
     * Given a parsed avro schema, encode a record for the given topic.
     * The schema is registered with the subject of 'topic-value'
     *
     * @param string $topic Topic name
     * @param AvroSchema $schema Avro Schema
     * @param array $record An object to serialize
     * @param bool $isKey If the record is a key
     *
     * @return string Encoded record with schema ID as bytes
     */
    public function encodeRecordWithSchema($topic, AvroSchema $schema, array $record, $isKey = false)
    {
        $suffix = $isKey ? '-key' : '-value';
        $subject = $topic.$suffix;

        try {
            $id = $this->registry->getSchemaId($subject, $schema);
        } catch (\RuntimeException $e) {
            if ($this->registerMissingSchemas) {
                $this->registry->register($subject, $schema);
                $id = $this->registry->getSchemaId($subject, $schema);
            } else {
                throw $e;
            }
        }
        // TODO: do we have to do this on every encodeRecordWithSchema call?
        $this->idToWriters[$id] = new AvroIODatumWriter($schema);

        return $this->encodeRecordWithSchemaId($id, $record, $isKey);
    }

    /**
     * Decode a message from kafka that has been encoded for use with the schema registry.
     *
     * @param string $message
     *
     * @return array
     */
    public function decodeMessage($message)
    {
        if (strlen($message) < 5) {
            throw new \RuntimeException('Message is too small to decode');
        }

        $io = new AvroStringIO($message);

        $header = unpack('Cmagic/Nid', $io->read(5));

        $magic = $header['magic'];
        if (static::MAGIC_BYTE !== $magic) {
            throw new \RuntimeException('Message does not start with magic byte');
        }

        $id = $header['id'];
        $decoder = $this->getDecoderById($id);

        return $decoder($io);
    }

    private function getDecoderById($schemaId)
    {
        if (isset($this->idToDecoderFunc[$schemaId])) {
            return $this->idToDecoderFunc[$schemaId];
        }

        $schema = $this->registry->getById($schemaId);

        $reader = new AvroIODatumReader($schema);

        $this->idToDecoderFunc[$schemaId] = function(AvroIO $io) use ($reader) {
            return $reader->read(new AvroIOBinaryDecoder($io));
        };

        return $this->idToDecoderFunc[$schemaId];
    }

}
