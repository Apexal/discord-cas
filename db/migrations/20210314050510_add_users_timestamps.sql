-- migrate:up
ALTER TABLE users ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- migrate:down

ALTER TABLE users DROP COLUMN created_at;