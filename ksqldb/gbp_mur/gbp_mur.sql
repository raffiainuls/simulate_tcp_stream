CREATE STREAM gbp_mur_data
WITH (
    KAFKA_TOPIC = 'gbp_mur_data',
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
where symbol = 'GBP/MUR'
PARTITION BY datetime + '_' + symbol 
EMIT CHANGES
