-- migrate:up
ALTER TABLE clients ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- migrate:down

ALTER TABLE clients DROP COLUMN created_at;