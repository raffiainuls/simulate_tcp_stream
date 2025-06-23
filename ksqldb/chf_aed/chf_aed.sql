CREATE STREAM chf_aed_data
WITH (
    KAFKA_TOPIC = 'chf_aed_data',
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
where symbol = 'CHF/AED'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
