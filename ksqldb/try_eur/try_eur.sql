CREATE STREAM try_eur_data
WITH (
    KAFKA_TOPIC = 'try_eur_data',
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
where symbol = 'TRY/EUR'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
