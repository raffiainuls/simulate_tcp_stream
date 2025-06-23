CREATE STREAM krw_cny_data
WITH (
    KAFKA_TOPIC = 'krw_cny_data',
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
where symbol = 'KRW/CNY'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
