-- migrate:up
CREATE TABLE "clients" (
  "client_id" SERIAL PRIMARY KEY,
  "is_enabled" boolean NOT NULL DEFAULT true,
  "name" varchar NOT NULL,
  "welcome_message" text,
  "discord_server_id" int NOT NULL,
  "discord_rpi_role_id" int NOT NULL,
  "discord_non_rpi_role_id" int,
  "contact_information" varchar,
  "is_rcs_id_in_nickname" boolean NOT NULL DEFAULT true,
  "is_public" boolean NOT NULL DEFAULT false
);

COMMENT ON COLUMN "clients"."is_enabled" IS 'Whether users can currently join through this portal';
COMMENT ON COLUMN "clients"."name" IS 'Public-facing name';
COMMENT ON COLUMN "clients"."welcome_message" IS 'Optional display message on client page';
COMMENT ON COLUMN "clients"."discord_server_id" IS 'Unique ID of Discord server for client';
COMMENT ON COLUMN "clients"."discord_rpi_role_id" IS 'Unique ID of role on Discord server for client to give to verified RPI users';
COMMENT ON COLUMN "clients"."discord_rpi_role_id" IS 'Unique ID of role on Discord server for client to give to external (non-RPI) users';
COMMENT ON COLUMN "clients"."is_rcs_id_in_nickname" IS 'Whether or not member nicknames in client servers should include RCS IDs';
COMMENT ON COLUMN "clients"."contact_information" IS 'Who to reach out to about the client';
COMMENT ON COLUMN "clients"."is_public" IS 'Whether the server of the client shows on a listing for all users';

-- migrate:down
DROP TABLE "clients";
