-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---
-- object: admin | type: ROLE --
-- DROP ROLE IF EXISTS admin;
-- CREATE ROLE admin WITH 
-- 	ENCRYPTED PASSWORD 'supersecretpassword';
-- ddl-end --


-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: restaurant_db | type: DATABASE --
-- DROP DATABASE IF EXISTS restaurant_db;
-- CREATE DATABASE restaurant_db;
-- ddl-end --


-- object: public.user_roles | type: TYPE --
-- DROP TYPE IF EXISTS public.user_roles CASCADE;
CREATE TYPE public.user_roles AS
ENUM ('admin','manager','waiter','kitchen');
-- ddl-end --
ALTER TYPE public.user_roles OWNER TO admin;
-- ddl-end --

-- object: public.users | type: TABLE --
-- DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE public.users (
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name varchar(256) NOT NULL,
	email varchar(256) NOT NULL,
	phone varchar(64),
	role public.user_roles NOT NULL,
	hashed_password varchar(1024) NOT NULL,
	meta json,
	CONSTRAINT id_pk PRIMARY KEY (id),
	CONSTRAINT email_uq UNIQUE (email)
);
-- ddl-end --
ALTER TABLE public.users OWNER TO admin;
-- ddl-end --


