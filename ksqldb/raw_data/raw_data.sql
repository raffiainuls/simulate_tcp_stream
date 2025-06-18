CREATE STREAM raw_data_tcp (
  payload STRUCT<
    symbol STRING,
    datetime STRING,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    open DOUBLE
  >
) WITH (
  KAFKA_TOPIC = 'raw_data_tcp',
  VALUE_FORMAT = 'JSON'
);
