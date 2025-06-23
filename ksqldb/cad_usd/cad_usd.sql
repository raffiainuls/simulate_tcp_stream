CREATE STREAM cad_usd_data
WITH (
    KAFKA_TOPIC = 'cad_usd_data',
    VALUE_FORMAT = 'JSON'
) AS
SELECT
  symbol,
  datetime,
  high,
  low,
  close,
  open,
  datetime + '_' + symbol AS composite_key
FROM clean_data_tcp
where symbol = 'CAD/USD'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
