-- Table: public.OsauhingAPP_isikud
-- DROP TABLE IF EXISTS public."OsauhingAPP_isikud";
CREATE TABLE IF NOT EXISTS public."OsauhingAPP_isikud"
(
    id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    isikutyyp character varying(1) COLLATE pg_catalog."default" NOT NULL,
    isosauhing boolean NOT NULL,
    nimi character varying(100) COLLATE pg_catalog."default" NOT NULL,
    perenimi character varying(100) COLLATE pg_catalog."default",
    kood character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "OsauhingAPP_isikud_pkey" PRIMARY KEY (id),
    CONSTRAINT "OsauhingAPP_isikud_kood_key" UNIQUE (kood)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."OsauhingAPP_isikud"
    OWNER to mqrfmqva;
-- Index: OsauhingAPP_isikud_kood_d9416e74_like

-- DROP INDEX IF EXISTS public."OsauhingAPP_isikud_kood_d9416e74_like";

CREATE INDEX IF NOT EXISTS "OsauhingAPP_isikud_kood_d9416e74_like"
    ON public."OsauhingAPP_isikud" USING btree
    (kood COLLATE pg_catalog."default" varchar_pattern_ops ASC NULLS LAST)
    TABLESPACE pg_default;
GO

-- Table: public.OsauhingAPP_osauhing
-- DROP TABLE IF EXISTS public."OsauhingAPP_osauhing";
CREATE TABLE IF NOT EXISTS public."OsauhingAPP_osauhing"
(
    id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    asutamisekp date NOT NULL,
    kogukapital integer NOT NULL,
    isik_id bigint NOT NULL,
    CONSTRAINT "OsauhingAPP_osauhing_pkey" PRIMARY KEY (id),
    CONSTRAINT "OsauhingAPP_osauhing_isik_id_443367f7_fk_OsauhingAPP_isikud_id" FOREIGN KEY (isik_id)
        REFERENCES public."OsauhingAPP_isikud" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."OsauhingAPP_osauhing"
    OWNER to mqrfmqva;
-- Index: OsauhingAPP_osauhing_isik_id_443367f7

-- DROP INDEX IF EXISTS public."OsauhingAPP_osauhing_isik_id_443367f7";

CREATE INDEX IF NOT EXISTS "OsauhingAPP_osauhing_isik_id_443367f7"
    ON public."OsauhingAPP_osauhing" USING btree
    (isik_id ASC NULLS LAST)
    TABLESPACE pg_default;
GO

-- Table: public.OsauhingAPP_osauhing_isikud
-- DROP TABLE IF EXISTS public."OsauhingAPP_osauhing_isikud";
CREATE TABLE IF NOT EXISTS public."OsauhingAPP_osauhing_isikud"
(
    id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "osauhinguOsa" integer NOT NULL,
    isasutaja boolean NOT NULL,
    isik_id bigint NOT NULL,
    osauhing_id bigint NOT NULL,
    CONSTRAINT "OsauhingAPP_osauhing_isikud_pkey" PRIMARY KEY (id),
    CONSTRAINT "OsauhingAPP_osauhing_isik_id_058545ab_fk_OsauhingA" FOREIGN KEY (isik_id)
        REFERENCES public."OsauhingAPP_isikud" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "OsauhingAPP_osauhing_osauhing_id_9b4d22d7_fk_OsauhingA" FOREIGN KEY (osauhing_id)
        REFERENCES public."OsauhingAPP_osauhing" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."OsauhingAPP_osauhing_isikud"
    OWNER to mqrfmqva;
-- Index: OsauhingAPP_osauhing_isikud_isik_id_058545ab

-- DROP INDEX IF EXISTS public."OsauhingAPP_osauhing_isikud_isik_id_058545ab";

CREATE INDEX IF NOT EXISTS "OsauhingAPP_osauhing_isikud_isik_id_058545ab"
    ON public."OsauhingAPP_osauhing_isikud" USING btree
    (isik_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: OsauhingAPP_osauhing_isikud_osauhing_id_9b4d22d7

-- DROP INDEX IF EXISTS public."OsauhingAPP_osauhing_isikud_osauhing_id_9b4d22d7";

CREATE INDEX IF NOT EXISTS "OsauhingAPP_osauhing_isikud_osauhing_id_9b4d22d7"
    ON public."OsauhingAPP_osauhing_isikud" USING btree
    (osauhing_id ASC NULLS LAST)
    TABLESPACE pg_default;