-- migrate:up
SET timezone = 'America/New_York';

-- migrate:down

SET timezone TO 'UTC';