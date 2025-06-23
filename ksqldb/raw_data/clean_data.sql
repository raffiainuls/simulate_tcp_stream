CREATE STREAM clean_data_tcp
WITH (
    KAFKA_TOPIC = 'clean_data_tcp',
    VALUE_FORMAT = 'JSON'
) AS
SELECT
  payload->symbol   AS symbol,
  payload->datetime AS datetime,
  payload->high     AS high,
  payload->low      AS low,
  payload->close    AS close,
  payload->open     AS open,
  payload->datetime + '_' + payload->symbol AS composite_key
FROM raw_data_tcp
PARTITION BY payload->datetime + '_' + payload->symbol
