CREATE STREAM zar_kes_data
WITH (
    KAFKA_TOPIC = 'zar_kes_data',
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
where symbol = 'ZAR/KES'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
