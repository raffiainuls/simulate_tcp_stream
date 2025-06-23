CREATE STREAM usd_cny_data
WITH (
    KAFKA_TOPIC = 'usd_cny_data',
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
where symbol = 'USD/CNY'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
