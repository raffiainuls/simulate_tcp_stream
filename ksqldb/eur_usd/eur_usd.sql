CREATE STREAM eur_usd_data
WITH (
    KAFKA_TOPIC = 'eur_usd_data',
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
where symbol = 'EUR/USD'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
