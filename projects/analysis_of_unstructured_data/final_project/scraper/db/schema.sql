SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(128) NOT NULL
);


--
-- Name: tweet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tweet (
    id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    tweeted_at timestamp with time zone NOT NULL,
    text character varying NOT NULL,
    replies integer NOT NULL,
    retweets integer NOT NULL,
    likes integer NOT NULL,
    views integer NOT NULL,
    user_handle character varying NOT NULL,
    parent_id integer
);


--
-- Name: user_; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_ (
    handle character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    name character varying NOT NULL,
    description character varying,
    following integer NOT NULL,
    followers integer NOT NULL
);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: tweet tweet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweet
    ADD CONSTRAINT tweet_pkey PRIMARY KEY (id);


--
-- Name: user_ user__pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_
    ADD CONSTRAINT user__pkey PRIMARY KEY (handle);


--
-- Name: tweet fk_self; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweet
    ADD CONSTRAINT fk_self FOREIGN KEY (parent_id) REFERENCES public.tweet(id);


--
-- Name: tweet fk_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tweet
    ADD CONSTRAINT fk_user FOREIGN KEY (user_handle) REFERENCES public.user_(handle);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20241126174911');
