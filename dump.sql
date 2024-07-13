--
-- PostgreSQL database dump
--

-- Dumped from database version 13.14 (Debian 13.14-1.pgdg120+2)
-- Dumped by pg_dump version 13.14 (Debian 13.14-1.pgdg120+2)

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
-- Name: dailyclimate; Type: TABLE; Schema: public; Owner: airflow
--

CREATE TABLE public.dailyclimate (
    id integer NOT NULL,
    idloc integer NOT NULL,
    tempc numeric(5,2),
    windkph numeric(5,2),
    winddeg integer,
    pressmb numeric(7,2),
    hum integer,
    uv numeric(3,1)
);


ALTER TABLE public.dailyclimate OWNER TO airflow;

--
-- Name: dailyclimate_id_seq; Type: SEQUENCE; Schema: public; Owner: airflow
--

CREATE SEQUENCE public.dailyclimate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dailyclimate_id_seq OWNER TO airflow;

--
-- Name: dailyclimate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: airflow
--

ALTER SEQUENCE public.dailyclimate_id_seq OWNED BY public.dailyclimate.id;


--
-- Name: stationlocation; Type: TABLE; Schema: public; Owner: airflow
--

CREATE TABLE public.stationlocation (
    id integer NOT NULL,
    lat numeric(9,6) NOT NULL,
    long numeric(9,6) NOT NULL,
    name character varying(255)
);


ALTER TABLE public.stationlocation OWNER TO airflow;

--
-- Name: stationlocation_id_seq; Type: SEQUENCE; Schema: public; Owner: airflow
--

CREATE SEQUENCE public.stationlocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stationlocation_id_seq OWNER TO airflow;

--
-- Name: stationlocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: airflow
--

ALTER SEQUENCE public.stationlocation_id_seq OWNED BY public.stationlocation.id;


--
-- Name: dailyclimate id; Type: DEFAULT; Schema: public; Owner: airflow
--

ALTER TABLE ONLY public.dailyclimate ALTER COLUMN id SET DEFAULT nextval('public.dailyclimate_id_seq'::regclass);


--
-- Name: stationlocation id; Type: DEFAULT; Schema: public; Owner: airflow
--

ALTER TABLE ONLY public.stationlocation ALTER COLUMN id SET DEFAULT nextval('public.stationlocation_id_seq'::regclass);


--
-- Data for Name: dailyclimate; Type: TABLE DATA; Schema: public; Owner: airflow
--

COPY public.dailyclimate (id, idloc, tempc, windkph, winddeg, pressmb, hum, uv) FROM stdin;
\.


--
-- Data for Name: stationlocation; Type: TABLE DATA; Schema: public; Owner: airflow
--

COPY public.stationlocation (id, lat, long, name) FROM stdin;
1	1.266557	117.819003	Station 1
2	1.252922	117.814700	Station 2
3	1.252656	117.828769	Station 3
4	1.253043	117.846616	Station 4
5	1.238490	117.846616	Station 5
6	1.238490	117.857027	Station 6
7	1.232453	117.864195	Station 7
8	1.227730	117.873833	Station 8
9	1.213578	117.845952	Station 9
10	1.242022	117.870190	Station 10
11	1.258019	117.867200	Station 11
12	1.267978	117.881793	Station 12
13	1.259847	117.890257	Station 13
14	1.242930	117.898458	Station 14
15	1.231917	117.899757	Station 15
16	1.278993	117.879321	Station 16
17	1.272297	117.904461	Station 17
18	1.284355	117.918273	Station 18
19	1.266913	117.928167	Station 19
20	1.246721	117.932198	Station 20
21	1.249611	117.916307	Station 21
22	1.258661	117.907452	Station 22
23	1.211997	117.870832	Station 23
\.


--
-- Name: dailyclimate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: airflow
--

SELECT pg_catalog.setval('public.dailyclimate_id_seq', 1, false);


--
-- Name: stationlocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: airflow
--

SELECT pg_catalog.setval('public.stationlocation_id_seq', 23, true);


--
-- Name: dailyclimate dailyclimate_pkey; Type: CONSTRAINT; Schema: public; Owner: airflow
--

ALTER TABLE ONLY public.dailyclimate
    ADD CONSTRAINT dailyclimate_pkey PRIMARY KEY (id);


--
-- Name: stationlocation stationlocation_pkey; Type: CONSTRAINT; Schema: public; Owner: airflow
--

ALTER TABLE ONLY public.stationlocation
    ADD CONSTRAINT stationlocation_pkey PRIMARY KEY (id);


--
-- Name: dailyclimate dailyclimate_idloc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: airflow
--

ALTER TABLE ONLY public.dailyclimate
    ADD CONSTRAINT dailyclimate_idloc_fkey FOREIGN KEY (idloc) REFERENCES public.stationlocation(id);


--
-- PostgreSQL database dump complete
--

