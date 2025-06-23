CREATE STREAM ils_vef_data
WITH (
    KAFKA_TOPIC = 'ils_vef_data',
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
where symbol = 'ILS/VEF'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
