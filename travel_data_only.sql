--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Debian 14.9-1.pgdg110+1)
-- Dumped by pg_dump version 14.9 (Debian 14.9-1.pgdg110+1)

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

--
-- Data for Name: accommodations_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accommodations_categories (id, name, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: continents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.continents (id, name, code, name_code, background_image, logo, description, description_code, status, created_date, updated_date) FROM stdin;
2	Europe	EU	continent.eu	https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=800&quot	https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg	\N	\N	1	2025-05-24	\N
4	North America	NA	continent.na	https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=800&quot	https://upload.wikimedia.org/wikipedia/commons/4/43/Location_North_America.svg	\N	\N	1	2025-05-24	\N
7	Oceania	OC	continent.oc	https://images.unsplash.com/photo-1507699622108-4be3abd695ad?q=80&w=800&quot	https://upload.wikimedia.org/wikipedia/commons/8/8e/Location_Oceania.svg	\N	\N	1	2025-05-24	\N
6	Africa	AF	continent.af	https://images.unsplash.com/photo-1523805009345-7448845a9e53?q=80&w=800&quot	https://upload.wikimedia.org/wikipedia/commons/5/51/Flag_of_the_African_Union.svg	\N	\N	1	2025-05-24	\N
1	Asia	AS	continent.as	https://images.unsplash.com/photo-1535139262971-c51845709a48?q=80&w=800&quot	https://upload.wikimedia.org/wikipedia/commons/e/e8/Location_Asia.svg	\N	\N	1	2025-05-22	\N
5	South America	SA	continent.sa	https://www.cuddlynest.com/blog/wp-content/uploads/2021/01/rio_de_janeiro.jpg	https://upload.wikimedia.org/wikipedia/commons/2/29/Location_South_America.svg	\N	\N	1	2025-05-24	\N
8	Antarctica	AN	continent.an	https://cdn.expeditions.com/globalassets/travel-guides/antarctica/seo-016-how-to-travel-to-antarctica-how-to-get-there-and-what-to-know/large-rgb-lex-ships-ng-endurace--resolution-exterior---antarctica-jb-dji-0625.jpg?width=1920&height=1080&mode=crop&scale=none&quality=50	https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Antarctica.svg	\N	\N	1	2025-05-24	\N
\.


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries (id, code, name, name_code, description, description_code, background_image, logo, status, created_date, updated_date, continent_id) FROM stdin;
408	AG	Antigua and Barbuda	country.atg.name	Island country in the West Indies.	country.atg.desc	https://example.com/img/ag.jpg	https://upload.wikimedia.org/wikipedia/commons/8/89/Flag_of_Antigua_and_Barbuda.svg	1	2025-05-24	\N	4
409	BS	Bahamas	country.bhs.name	Archipelagic state in the West Indies.	country.bhs.desc	https://example.com/img/bs.jpg	https://upload.wikimedia.org/wikipedia/commons/9/93/Flag_of_the_Bahamas.svg	1	2025-05-24	\N	4
410	BB	Barbados	country.brb.name	Island country in the Lesser Antilles.	country.brb.desc	https://example.com/img/bb.jpg	https://upload.wikimedia.org/wikipedia/commons/e/ef/Flag_of_Barbados.svg	1	2025-05-24	\N	4
411	BZ	Belize	country.blz.name	Country on the northeastern coast of Central America.	country.blz.desc	https://example.com/img/bz.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e7/Flag_of_Belize.svg	1	2025-05-24	\N	4
412	CA	Canada	country.can.name	Country in North America.	country.can.desc	https://example.com/img/ca.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Canada_%28Pantone%29.svg	1	2025-05-24	\N	4
413	CR	Costa Rica	country.cri.name	Country in Central America.	country.cri.desc	https://example.com/img/cr.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Costa_Rica_%28state%29.svg	1	2025-05-24	\N	4
414	CU	Cuba	country.cub.name	Island country in the Caribbean.	country.cub.desc	https://example.com/img/cu.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bd/Flag_of_Cuba.svg	1	2025-05-24	\N	4
415	DM	Dominica	country.dma.name	Island country in the Caribbean.	country.dma.desc	https://example.com/img/dm.jpg	https://upload.wikimedia.org/wikipedia/commons/c/c4/Flag_of_Dominica.svg	1	2025-05-24	\N	4
416	DO	Dominican Republic	country.dom.name	Country on the island of Hispaniola.	country.dom.desc	https://example.com/img/do.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_the_Dominican_Republic.svg	1	2025-05-24	\N	4
417	SV	El Salvador	country.slv.name	Country in Central America.	country.slv.desc	https://example.com/img/sv.jpg	https://upload.wikimedia.org/wikipedia/commons/3/34/Flag_of_El_Salvador.svg	1	2025-05-24	\N	4
418	GD	Grenada	country.grd.name	Island country in the West Indies.	country.grd.desc	https://example.com/img/gd.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Grenada.svg	1	2025-05-24	\N	4
419	GT	Guatemala	country.gtm.name	Country in Central America.	country.gtm.desc	https://example.com/img/gt.jpg	https://upload.wikimedia.org/wikipedia/commons/e/ec/Flag_of_Guatemala.svg	1	2025-05-24	\N	4
420	HT	Haiti	country.hti.name	Country on the island of Hispaniola.	country.hti.desc	https://example.com/img/ht.jpg	https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg	1	2025-05-24	\N	4
421	HN	Honduras	country.hnd.name	Country in Central America.	country.hnd.desc	https://example.com/img/hn.jpg	https://upload.wikimedia.org/wikipedia/commons/8/82/Flag_of_Honduras.svg	1	2025-05-24	\N	4
422	JM	Jamaica	country.jam.name	Island country in the Caribbean Sea.	country.jam.desc	https://example.com/img/jm.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0a/Flag_of_Jamaica.svg	1	2025-05-24	\N	4
423	MX	Mexico	country.mex.name	Country in the southern portion of North America.	country.mex.desc	https://example.com/img/mx.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fc/Flag_of_Mexico.svg	1	2025-05-24	\N	4
424	NI	Nicaragua	country.nic.name	Country in Central America.	country.nic.desc	https://example.com/img/ni.jpg	https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Nicaragua.svg	1	2025-05-24	\N	4
425	PA	Panama	country.pan.name	Transcontinental country in Central America.	country.pan.desc	https://example.com/img/pa.jpg	https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag_of_Panama.svg	1	2025-05-24	\N	4
426	KN	Saint Kitts and Nevis	country.kna.name	Dual-island country in the West Indies.	country.kna.desc	https://example.com/img/kn.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Saint_Kitts_and_Nevis.svg	1	2025-05-24	\N	4
427	LC	Saint Lucia	country.lca.name	Island country in the West Indies.	country.lca.desc	https://example.com/img/lc.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Saint_Lucia.svg	1	2025-05-24	\N	4
428	VC	Saint Vincent and the Grenadines	country.vct.name	Island country in the Caribbean.	country.vct.desc	https://example.com/img/vc.jpg	https://upload.wikimedia.org/wikipedia/commons/6/6d/Flag_of_Saint_Vincent_and_the_Grenadines.svg	1	2025-05-24	\N	4
429	TT	Trinidad and Tobago	country.tto.name	Dual-island country in the southern Caribbean.	country.tto.desc	https://example.com/img/tt.jpg	https://upload.wikimedia.org/wikipedia/commons/6/64/Flag_of_Trinidad_and_Tobago.svg	1	2025-05-24	\N	4
430	US	United States	country.usa.name	Country primarily located in North America.	country.usa.desc	https://example.com/img/us.jpg	https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg	1	2025-05-24	\N	4
431	PR	Puerto Rico	territory.pri.name	Unincorporated territory of the United States.	territory.pri.desc	https://example.com/img/pr.jpg	https://upload.wikimedia.org/wikipedia/commons/2/28/Flag_of_Puerto_Rico.svg	1	2025-05-24	\N	4
432	GL	Greenland	territory.grl.name	Autonomous territory of Denmark.	territory.grl.desc	https://example.com/img/gl.jpg	https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_Greenland.svg	1	2025-05-24	\N	4
433	BM	Bermuda	territory.bmu.name	British Overseas Territory.	territory.bmu.desc	https://example.com/img/bm.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bf/Flag_of_Bermuda.svg	1	2025-05-24	\N	4
434	VI	US Virgin Islands	territory.vir.name	Unincorporated territory of the United States.	territory.vir.desc	https://example.com/img/vi.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f8/Flag_of_the_United_States_Virgin_Islands.svg	1	2025-05-24	\N	4
435	KY	Cayman Islands	territory.cym.name	British Overseas Territory.	territory.cym.desc	https://example.com/img/ky.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_the_Cayman_Islands.svg	1	2025-05-24	\N	4
436	AR	Argentina	country.arg.name	Country in the southern half of South America.	country.arg.desc	https://example.com/img/ar.jpg	https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg	1	2025-05-24	\N	5
437	BO	Bolivia	country.bol.name	Landlocked country in western-central South America.	country.bol.desc	https://example.com/img/bo.jpg	https://upload.wikimedia.org/wikipedia/commons/d/de/Flag_of_Bolivia_%28state%29.svg	1	2025-05-24	\N	5
438	BR	Brazil	country.bra.name	Largest country in both South America and Latin America.	country.bra.desc	https://example.com/img/br.jpg	https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg	1	2025-05-24	\N	5
439	CL	Chile	country.chl.name	Country in western South America.	country.chl.desc	https://example.com/img/cl.jpg	https://upload.wikimedia.org/wikipedia/commons/7/78/Flag_of_Chile.svg	1	2025-05-24	\N	5
440	CO	Colombia	country.col.name	Country in northwestern South America.	country.col.desc	https://example.com/img/co.jpg	https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg	1	2025-05-24	\N	5
441	EC	Ecuador	country.ecu.name	Country in northwestern South America.	country.ecu.desc	https://example.com/img/ec.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e8/Flag_of_Ecuador.svg	1	2025-05-24	\N	5
442	GY	Guyana	country.guy.name	Country on the northern mainland of South America.	country.guy.desc	https://example.com/img/gy.jpg	https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Guyana.svg	1	2025-05-24	\N	5
443	PY	Paraguay	country.pry.name	Landlocked country in central South America.	country.pry.desc	https://example.com/img/py.jpg	https://upload.wikimedia.org/wikipedia/commons/2/27/Flag_of_Paraguay.svg	1	2025-05-24	\N	5
444	PE	Peru	country.per.name	Country in western South America.	country.per.desc	https://example.com/img/pe.jpg	https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Peru.svg	1	2025-05-24	\N	5
445	SR	Suriname	country.sur.name	Country on the northeastern Atlantic coast of South America.	country.sur.desc	https://example.com/img/sr.jpg	https://upload.wikimedia.org/wikipedia/commons/6/60/Flag_of_Suriname.svg	1	2025-05-24	\N	5
446	UY	Uruguay	country.ury.name	Country in the southeastern region of South America.	country.ury.desc	https://example.com/img/uy.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Uruguay.svg	1	2025-05-24	\N	5
447	VE	Venezuela	country.ven.name	Country on the northern coast of South America.	country.ven.desc	https://example.com/img/ve.jpg	https://upload.wikimedia.org/wikipedia/commons/0/06/Flag_of_Venezuela.svg	1	2025-05-24	\N	5
448	GF	French Guiana	territory.guf.name	Overseas department of France.	territory.guf.desc	https://example.com/img/gf.jpg	https://upload.wikimedia.org/wikipedia/commons/2/20/Flag_of_French_Guiana.svg	1	2025-05-24	\N	5
449	FK	Falkland Islands	territory.flk.name	British Overseas Territory.	territory.flk.desc	https://example.com/img/fk.jpg	https://upload.wikimedia.org/wikipedia/commons/8/83/Flag_of_the_Falkland_Islands.svg	1	2025-05-24	\N	5
529	AQ-GEN	Antarctica (General)	antarctica.general.name	The continent of Antarctica, governed by the Antarctic Treaty System.	antarctica.general.desc	https://example.com/img/aq_general.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f2/Flag_of_Antarctica_%28Graham_Bartram%29.svg	1	2025-05-24	\N	8
530	AQ-BAT	British Antarctic Territory	antarctica.bat.name	A British Overseas Territory claimed by the United Kingdom.	antarctica.bat.desc	https://example.com/img/aq_bat.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_the_British_Antarctic_Territory.svg	1	2025-05-24	\N	8
531	AQ-TAAF	Adélie Land (French Southern and Antarctic Lands)	antarctica.taaf.name	Claimed by France as part of the French Southern and Antarctic Lands (TAAF).	antarctica.taaf.desc	https://example.com/img/aq_taaf.jpg	https://upload.wikimedia.org/wikipedia/commons/a/a7/Flag_of_the_French_Southern_and_Antarctic_Lands.svg	1	2025-05-24	\N	8
532	AQ-RD	Ross Dependency	antarctica.ross.name	Claimed by New Zealand.	antarctica.ross.desc	https://example.com/img/aq_ross.jpg	https://upload.wikimedia.org/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg	1	2025-05-24	\N	8
533	AQ-AAT	Australian Antarctic Territory	antarctica.aat.name	Claimed by Australia.	antarctica.aat.desc	https://example.com/img/aq_aat.jpg	https://upload.wikimedia.org/wikipedia/commons/8/88/Flag_of_Australia_%28converted%29.svg	1	2025-05-24	\N	8
534	AQ-QML	Queen Maud Land	antarctica.qml.name	Claimed by Norway.	antarctica.qml.desc	https://example.com/img/aq_qml.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg	1	2025-05-24	\N	8
535	AQ-PII	Peter I Island	antarctica.pii.name	Claimed by Norway.	antarctica.pii.desc	https://example.com/img/aq_pii.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg	1	2025-05-24	\N	8
536	AQ-CHL	Chilean Antarctic Territory	antarctica.chl.name	Claimed by Chile.	antarctica.chl.desc	https://example.com/img/aq_chl.jpg	https://upload.wikimedia.org/wikipedia/commons/1/13/Flag_of_Magallanes_Region%2C_Chile.svg	1	2025-05-24	\N	8
537	AQ-ARG	Argentine Antarctica	antarctica.arg.name	Claimed by Argentina.	antarctica.arg.desc	https://example.com/img/aq_arg.jpg	https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg	1	2025-05-24	\N	8
538	AQ-MBL	Marie Byrd Land (Unclaimed)	antarctica.mbl.name	The largest single unclaimed territory on Earth.	antarctica.mbl.desc	https://example.com/img/aq_mbl.jpg	\N	1	2025-05-24	\N	8
358	AF	Afghanistan	country.afg.name	A country in South-Central Asia.	country.afg.desc	https://example.com/img/af.jpg	https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_the_Taliban.svg	1	2025-05-22	2025-05-26	1
361	BH	Bahrain	country.bhr.name	An island country in Western Asia.	country.bhr.desc	https://example.com/img/bh.jpg	https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Bahrain.svg	1	2025-05-22	2025-05-26	1
366	CN	China	country.chn.name	A country in East Asia.	country.chn.desc	https://example.com/img/cn.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg	1	2025-05-22	2025-05-26	1
373	IQ	Iraq	country.irq.name	A country in Western Asia.	country.irq.desc	https://example.com/img/iq.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f6/Flag_of_Iraq.svg	1	2025-05-22	2025-05-26	1
379	KG	Kyrgyzstan	country.kgz.name	A country in Central Asia.	country.kgz.desc	https://example.com/img/kg.jpg	https://upload.wikimedia.org/wikipedia/commons/c/c7/Flag_of_Kyrgyzstan.svg	1	2025-05-22	2025-05-26	1
384	MV	Maldives	country.mdv.name	An island nation in South Asia.	country.mdv.desc	https://example.com/img/mv.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Maldives.svg	1	2025-05-22	2025-05-26	1
2	VN	Vietnam	country.vnm.name	A country in Southeast Asia.	country.vnm.desc	https://example.com/img/vn.jpg	https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Vietnam.svg	1	2025-05-22	2025-05-26	1
541	AT	Austria	country.aut.name	A country in Central Europe.	country.aut.desc	https://example.com/img/at.jpg	https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Austria.svg	1	2025-05-24	2025-05-26	2
542	BY	Belarus	country.blr.name	A country in Eastern Europe.	country.blr.desc	https://example.com/img/by.jpg	https://upload.wikimedia.org/wikipedia/commons/8/85/Flag_of_Belarus.svg	1	2025-05-24	2025-05-26	2
543	BE	Belgium	country.bel.name	A country in Western Europe.	country.bel.desc	https://example.com/img/be.jpg	https://upload.wikimedia.org/wikipedia/commons/6/65/Flag_of_Belgium.svg	1	2025-05-24	2025-05-26	2
544	BA	Bosnia and Herzegovina	country.bih.name	A country in Southeast Europe.	country.bih.desc	https://example.com/img/ba.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bf/Flag_of_Bosnia_and_Herzegovina.svg	1	2025-05-24	2025-05-26	2
450	DZ	Algeria	country.dza.name	Country in North Africa.	country.dza.desc	https://example.com/img/dz.jpg	https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Algeria.svg	1	2025-05-24	\N	6
451	AO	Angola	country.ago.name	Country in Southern Africa.	country.ago.desc	https://example.com/img/ao.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9d/Flag_of_Angola.svg	1	2025-05-24	\N	6
452	BJ	Benin	country.ben.name	Country in West Africa.	country.ben.desc	https://example.com/img/bj.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0a/Flag_of_Benin.svg	1	2025-05-24	\N	6
453	BW	Botswana	country.bwa.name	Landlocked country in Southern Africa.	country.bwa.desc	https://example.com/img/bw.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_Botswana.svg	1	2025-05-24	\N	6
454	BF	Burkina Faso	country.bfa.name	Landlocked country in West Africa.	country.bfa.desc	https://example.com/img/bf.jpg	https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Burkina_Faso.svg	1	2025-05-24	\N	6
455	BI	Burundi	country.bdi.name	Landlocked country in the Great Rift Valley.	country.bdi.desc	https://example.com/img/bi.jpg	https://upload.wikimedia.org/wikipedia/commons/5/50/Flag_of_Burundi.svg	1	2025-05-24	\N	6
456	CV	Cabo Verde	country.cpv.name	Archipelago country in the central Atlantic Ocean.	country.cpv.desc	https://example.com/img/cv.jpg	https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Cape_Verde.svg	1	2025-05-24	\N	6
457	CM	Cameroon	country.cmr.name	Country in Central Africa.	country.cmr.desc	https://example.com/img/cm.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4f/Flag_of_Cameroon.svg	1	2025-05-24	\N	6
458	CF	Central African Republic	country.caf.name	Landlocked country in Central Africa.	country.caf.desc	https://example.com/img/cf.jpg	https://upload.wikimedia.org/wikipedia/commons/6/6f/Flag_of_the_Central_African_Republic.svg	1	2025-05-24	\N	6
459	TD	Chad	country.tcd.name	Landlocked country at the crossroads of North and Central Africa.	country.tcd.desc	https://example.com/img/td.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4b/Flag_of_Chad.svg	1	2025-05-24	\N	6
460	KM	Comoros	country.com.name	Archipelagic country in the Indian Ocean.	country.com.desc	https://example.com/img/km.jpg	https://upload.wikimedia.org/wikipedia/commons/9/94/Flag_of_the_Comoros.svg	1	2025-05-24	\N	6
461	CG	Congo, Republic of the	country.cog.name	Country in Central Africa (Brazzaville).	country.cog.desc	https://example.com/img/cg.jpg	https://upload.wikimedia.org/wikipedia/commons/9/92/Flag_of_the_Republic_of_the_Congo.svg	1	2025-05-24	\N	6
462	CD	Congo, Democratic Republic of the	country.cod.name	Country in Central Africa (Kinshasa).	country.cod.desc	https://example.com/img/cd.jpg	https://upload.wikimedia.org/wikipedia/commons/6/6f/Flag_of_the_Democratic_Republic_of_the_Congo.svg	1	2025-05-24	\N	6
463	CI	Côte d'Ivoire	country.civ.name	Country in West Africa (Ivory Coast).	country.civ.desc	https://example.com/img/ci.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_C%C3%B4te_d%27Ivoire.svg	1	2025-05-24	\N	6
464	DJ	Djibouti	country.dji.name	Country in the Horn of Africa.	country.dji.desc	https://example.com/img/dj.jpg	https://upload.wikimedia.org/wikipedia/commons/3/34/Flag_of_Djibouti.svg	1	2025-05-24	\N	6
465	EG	Egypt	country.egy.name	Transcontinental country linking northeast Africa with the Middle East.	country.egy.desc	https://example.com/img/eg.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Egypt.svg	1	2025-05-24	\N	6
466	GQ	Equatorial Guinea	country.gnq.name	Country in Central Africa.	country.gnq.desc	https://example.com/img/gq.jpg	https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Equatorial_Guinea.svg	1	2025-05-24	\N	6
467	ER	Eritrea	country.eri.name	Country in the Horn of Africa.	country.eri.desc	https://example.com/img/er.jpg	https://upload.wikimedia.org/wikipedia/commons/2/29/Flag_of_Eritrea.svg	1	2025-05-24	\N	6
468	SZ	Eswatini	country.swz.name	Landlocked country in Southern Africa (formerly Swaziland).	country.swz.desc	https://example.com/img/sz.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fb/Flag_of_Eswatini.svg	1	2025-05-24	\N	6
469	ET	Ethiopia	country.eth.name	Landlocked country in the Horn of Africa.	country.eth.desc	https://example.com/img/et.jpg	https://upload.wikimedia.org/wikipedia/commons/7/71/Flag_of_Ethiopia.svg	1	2025-05-24	\N	6
470	GA	Gabon	country.gab.name	Country on the Atlantic coast of Central Africa.	country.gab.desc	https://example.com/img/ga.jpg	https://upload.wikimedia.org/wikipedia/commons/0/04/Flag_of_Gabon.svg	1	2025-05-24	\N	6
471	GM	Gambia	country.gmb.name	Country in West Africa.	country.gmb.desc	https://example.com/img/gm.jpg	https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_The_Gambia.svg	1	2025-05-24	\N	6
472	GH	Ghana	country.gha.name	Country in West Africa.	country.gha.desc	https://example.com/img/gh.jpg	https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Ghana.svg	1	2025-05-24	\N	6
473	GN	Guinea	country.gin.name	Country in West Africa.	country.gin.desc	https://example.com/img/gn.jpg	https://upload.wikimedia.org/wikipedia/commons/e/ed/Flag_of_Guinea.svg	1	2025-05-24	\N	6
474	GW	Guinea-Bissau	country.gnb.name	Country in West Africa.	country.gnb.desc	https://example.com/img/gw.jpg	https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Guinea-Bissau.svg	1	2025-05-24	\N	6
475	KE	Kenya	country.ken.name	Country in East Africa.	country.ken.desc	https://example.com/img/ke.jpg	https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Kenya.svg	1	2025-05-24	\N	6
476	LS	Lesotho	country.lso.name	Enclaved country within South Africa.	country.lso.desc	https://example.com/img/ls.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4a/Flag_of_Lesotho.svg	1	2025-05-24	\N	6
477	LR	Liberia	country.lbr.name	Country on the West African coast.	country.lbr.desc	https://example.com/img/lr.jpg	https://upload.wikimedia.org/wikipedia/commons/b/b8/Flag_of_Liberia.svg	1	2025-05-24	\N	6
478	LY	Libya	country.lby.name	Country in the Maghreb region of North Africa.	country.lby.desc	https://example.com/img/ly.jpg	https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Libya.svg	1	2025-05-24	\N	6
479	MG	Madagascar	country.mdg.name	Island country in the Indian Ocean.	country.mdg.desc	https://example.com/img/mg.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Madagascar.svg	1	2025-05-24	\N	6
480	MW	Malawi	country.mwi.name	Landlocked country in Southeastern Africa.	country.mwi.desc	https://example.com/img/mw.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d1/Flag_of_Malawi.svg	1	2025-05-24	\N	6
481	ML	Mali	country.mli.name	Landlocked country in West Africa.	country.mli.desc	https://example.com/img/ml.jpg	https://upload.wikimedia.org/wikipedia/commons/9/92/Flag_of_Mali.svg	1	2025-05-24	\N	6
482	MR	Mauritania	country.mrt.name	Country in Northwest Africa.	country.mrt.desc	https://example.com/img/mr.jpg	https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg	1	2025-05-24	\N	6
483	MU	Mauritius	country.mus.name	Island nation in the Indian Ocean.	country.mus.desc	https://example.com/img/mu.jpg	https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Mauritius.svg	1	2025-05-24	\N	6
484	MA	Morocco	country.mar.name	Country in the Maghreb region of North Africa.	country.mar.desc	https://example.com/img/ma.jpg	https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg	1	2025-05-24	\N	6
485	MZ	Mozambique	country.moz.name	Country in Southeast Africa.	country.moz.desc	https://example.com/img/mz.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d0/Flag_of_Mozambique.svg	1	2025-05-24	\N	6
486	NA	Namibia	country.nam.name	Country in Southern Africa.	country.nam.desc	https://example.com/img/na.jpg	https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Namibia.svg	1	2025-05-24	\N	6
487	NE	Niger	country.ner.name	Landlocked country in West Africa.	country.ner.desc	https://example.com/img/ne.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f4/Flag_of_Niger.svg	1	2025-05-24	\N	6
488	NG	Nigeria	country.nga.name	Country in West Africa.	country.nga.desc	https://example.com/img/ng.jpg	https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_of_Nigeria.svg	1	2025-05-24	\N	6
489	RW	Rwanda	country.rwa.name	Landlocked country in the Great Rift Valley.	country.rwa.desc	https://example.com/img/rw.jpg	https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Rwanda.svg	1	2025-05-24	\N	6
490	ST	Sao Tome and Principe	country.stp.name	Island country in the Gulf of Guinea.	country.stp.desc	https://example.com/img/st.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4f/Flag_of_Sao_Tome_and_Principe.svg	1	2025-05-24	\N	6
491	SN	Senegal	country.sen.name	Country in West Africa.	country.sen.desc	https://example.com/img/sn.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_Senegal.svg	1	2025-05-24	\N	6
492	SC	Seychelles	country.syc.name	Archipelagic island country in the Indian Ocean.	country.syc.desc	https://example.com/img/sc.jpg	https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_Seychelles.svg	1	2025-05-24	\N	6
493	SL	Sierra Leone	country.sle.name	Country on the southwest coast of West Africa.	country.sle.desc	https://example.com/img/sl.jpg	https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Sierra_Leone.svg	1	2025-05-24	\N	6
494	SO	Somalia	country.som.name	Country in the Horn of Africa.	country.som.desc	https://example.com/img/so.jpg	https://upload.wikimedia.org/wikipedia/commons/a/a0/Flag_of_Somalia.svg	1	2025-05-24	\N	6
359	AM	Armenia	country.arm.name	A country in Western Asia.	country.arm.desc	https://example.com/img/am.jpg	https://upload.wikimedia.org/wikipedia/commons/2/2f/Flag_of_Armenia.svg	1	2025-05-22	2025-05-26	1
360	AZ	Azerbaijan	country.aze.name	A country in Western Asia.	country.aze.desc	https://example.com/img/az.jpg	https://upload.wikimedia.org/wikipedia/commons/d/dd/Flag_of_Azerbaijan.svg	1	2025-05-22	2025-05-26	1
362	BD	Bangladesh	country.bgd.name	A country in South Asia.	country.bgd.desc	https://example.com/img/bd.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f9/Flag_of_Bangladesh.svg	1	2025-05-22	2025-05-26	1
363	BT	Bhutan	country.btn.name	A kingdom in South Asia.	country.btn.desc	https://example.com/img/bt.jpg	https://upload.wikimedia.org/wikipedia/commons/9/91/Flag_of_Bhutan.svg	1	2025-05-22	2025-05-26	1
364	BN	Brunei Darussalam	country.brn.name	A nation on the island of Borneo.	country.brn.desc	https://example.com/img/bn.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9c/Flag_of_Brunei.svg	1	2025-05-22	2025-05-26	1
365	KH	Cambodia	country.khm.name	A country in Southeast Asia.	country.khm.desc	https://example.com/img/kh.jpg	https://upload.wikimedia.org/wikipedia/commons/8/83/Flag_of_Cambodia.svg	1	2025-05-22	2025-05-26	1
367	CY	Cyprus	country.cyp.name	An island country in the Eastern Mediterranean.	country.cyp.desc	https://example.com/img/cy.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Cyprus.svg	1	2025-05-22	2025-05-26	1
368	GE	Georgia	country.geo.name	A country at the intersection of Europe and Asia.	country.geo.desc	https://example.com/img/ge.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Georgia.svg	1	2025-05-22	2025-05-26	1
369	HK	Hong Kong	country.hkg.name	A Special Administrative Region of China.	country.hkg.desc	https://example.com/img/hk.jpg	https://upload.wikimedia.org/wikipedia/commons/5/5b/Flag_of_Hong_Kong.svg	1	2025-05-22	2025-05-26	1
370	IN	India	country.ind.name	A country in South Asia.	country.ind.desc	https://example.com/img/in.jpg	https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg	1	2025-05-22	2025-05-26	1
371	ID	Indonesia	country.idn.name	A country in Southeast Asia and Oceania.	country.idn.desc	https://example.com/img/id.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Indonesia.svg	1	2025-05-22	2025-05-26	1
372	IR	Iran	country.irn.name	A country in Western Asia.	country.irn.desc	https://example.com/img/ir.jpg	https://upload.wikimedia.org/wikipedia/commons/c/ca/Flag_of_Iran.svg	1	2025-05-22	2025-05-26	1
374	IL	Israel	country.isr.name	A country in the Middle East.	country.isr.desc	https://example.com/img/il.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Israel.svg	1	2025-05-22	2025-05-26	1
375	JP	Japan	country.jpn.name	An island country in East Asia.	country.jpn.desc	https://example.com/img/jp.jpg	https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg	1	2025-05-22	2025-05-26	1
376	JO	Jordan	country.jor.name	An Arab country in Western Asia.	country.jor.desc	https://example.com/img/jo.jpg	https://upload.wikimedia.org/wikipedia/commons/c/c0/Flag_of_Jordan.svg	1	2025-05-22	2025-05-26	1
377	KZ	Kazakhstan	country.kaz.name	A transcontinental country mainly in Central Asia.	country.kaz.desc	https://example.com/img/kz.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d3/Flag_of_Kazakhstan.svg	1	2025-05-22	2025-05-26	1
378	KW	Kuwait	country.kwt.name	A country in Western Asia.	country.kwt.desc	https://example.com/img/kw.jpg	https://upload.wikimedia.org/wikipedia/commons/a/aa/Flag_of_Kuwait.svg	1	2025-05-22	2025-05-26	1
380	LA	Laos	country.lao.name	A country in Southeast Asia.	country.lao.desc	https://example.com/img/la.jpg	https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Laos.svg	1	2025-05-22	2025-05-26	1
381	LB	Lebanon	country.lbn.name	A country in Western Asia.	country.lbn.desc	https://example.com/img/lb.jpg	https://upload.wikimedia.org/wikipedia/commons/5/59/Flag_of_Lebanon.svg	1	2025-05-22	2025-05-26	1
382	MO	Macao	country.mac.name	A Special Administrative Region of China.	country.mac.desc	https://example.com/img/mo.jpg	https://upload.wikimedia.org/wikipedia/commons/6/63/Flag_of_Macau.svg	1	2025-05-22	2025-05-26	1
495	ZA	South Africa	country.zaf.name	Country on the southernmost tip of Africa.	country.zaf.desc	https://example.com/img/za.jpg	https://upload.wikimedia.org/wikipedia/commons/a/af/Flag_of_South_Africa.svg	1	2025-05-24	\N	6
496	SS	South Sudan	country.ssd.name	Landlocked country in East-Central Africa.	country.ssd.desc	https://example.com/img/ss.jpg	https://upload.wikimedia.org/wikipedia/commons/7/7a/Flag_of_South_Sudan.svg	1	2025-05-24	\N	6
497	SD	Sudan	country.sdn.name	Country in Northeast Africa.	country.sdn.desc	https://example.com/img/sd.jpg	https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Sudan.svg	1	2025-05-24	\N	6
498	TZ	Tanzania	country.tza.name	Country in East Africa.	country.tza.desc	https://example.com/img/tz.jpg	https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Tanzania.svg	1	2025-05-24	\N	6
499	TG	Togo	country.tgo.name	Country in West Africa.	country.tgo.desc	https://example.com/img/tg.jpg	https://upload.wikimedia.org/wikipedia/commons/6/68/Flag_of_Togo.svg	1	2025-05-24	\N	6
500	TN	Tunisia	country.tun.name	Country in the Maghreb region of North Africa.	country.tun.desc	https://example.com/img/tn.jpg	https://upload.wikimedia.org/wikipedia/commons/c/ce/Flag_of_Tunisia.svg	1	2025-05-24	\N	6
501	UG	Uganda	country.uga.name	Landlocked country in East Africa.	country.uga.desc	https://example.com/img/ug.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4e/Flag_of_Uganda.svg	1	2025-05-24	\N	6
502	ZM	Zambia	country.zmb.name	Landlocked country in Southern Africa.	country.zmb.desc	https://example.com/img/zm.jpg	https://upload.wikimedia.org/wikipedia/commons/0/06/Flag_of_Zambia.svg	1	2025-05-24	\N	6
503	ZW	Zimbabwe	country.zwe.name	Landlocked country in Southern Africa.	country.zwe.desc	https://example.com/img/zw.jpg	https://upload.wikimedia.org/wikipedia/commons/6/6a/Flag_of_Zimbabwe.svg	1	2025-05-24	\N	6
504	EH	Western Sahara	country.esh.name	Disputed territory in North Africa.	country.esh.desc	https://example.com/img/eh.jpg	https://upload.wikimedia.org/wikipedia/commons/2/26/Flag_of_the_Sahrawi_Arab_Democratic_Republic.svg	1	2025-05-24	\N	6
505	AU	Australia	country.aus.name	Country comprising the mainland of the Australian continent and Tasmania.	country.aus.desc	https://example.com/img/au.jpg	https://upload.wikimedia.org/wikipedia/commons/8/88/Flag_of_Australia_%28converted%29.svg	1	2025-05-24	\N	7
506	NZ	New Zealand	country.nzl.name	Island country in the southwestern Pacific Ocean.	country.nzl.desc	https://example.com/img/nz.jpg	https://upload.wikimedia.org/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg	1	2025-05-24	\N	7
507	PG	Papua New Guinea	country.png.name	Country in Oceania, occupying the eastern half of New Guinea.	country.png.desc	https://example.com/img/pg.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e3/Flag_of_Papua_New_Guinea.svg	1	2025-05-24	\N	7
508	FJ	Fiji	country.fji.name	Island country in Melanesia, South Pacific Ocean.	country.fji.desc	https://example.com/img/fj.jpg	https://upload.wikimedia.org/wikipedia/commons/b/ba/Flag_of_Fiji.svg	1	2025-05-24	\N	7
509	SB	Solomon Islands	country.slb.name	Country consisting of many islands in Oceania.	country.slb.desc	https://example.com/img/sb.jpg	https://upload.wikimedia.org/wikipedia/commons/7/74/Flag_of_the_Solomon_Islands.svg	1	2025-05-24	\N	7
510	VU	Vanuatu	country.vut.name	Pacific island country located in the South Pacific Ocean.	country.vut.desc	https://example.com/img/vu.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Vanuatu.svg	1	2025-05-24	\N	7
511	WS	Samoa	country.wsm.name	Polynesian island country.	country.wsm.desc	https://example.com/img/ws.jpg	https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Samoa.svg	1	2025-05-24	\N	7
512	KI	Kiribati	country.kir.name	Island nation in the central Pacific Ocean.	country.kir.desc	https://example.com/img/ki.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d3/Flag_of_Kiribati.svg	1	2025-05-24	\N	7
513	TO	Tonga	country.ton.name	Polynesian kingdom of more than 170 South Pacific islands.	country.ton.desc	https://example.com/img/to.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Tonga.svg	1	2025-05-24	\N	7
514	TV	Tuvalu	country.tuv.name	Island country in Polynesia.	country.tuv.desc	https://example.com/img/tv.jpg	https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Tuvalu.svg	1	2025-05-24	\N	7
515	MH	Marshall Islands	country.mhl.name	Island country near the Equator in the Pacific Ocean.	country.mhl.desc	https://example.com/img/mh.jpg	https://upload.wikimedia.org/wikipedia/commons/2/2e/Flag_of_the_Marshall_Islands.svg	1	2025-05-24	\N	7
516	FM	Micronesia, Federated States of	country.fsm.name	Island country in Oceania.	country.fsm.desc	https://example.com/img/fm.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e4/Flag_of_the_Federated_States_of_Micronesia.svg	1	2025-05-24	\N	7
517	PW	Palau	country.plw.name	Island country located in the western Pacific Ocean.	country.plw.desc	https://example.com/img/pw.jpg	https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Palau.svg	1	2025-05-24	\N	7
518	NR	Nauru	country.nru.name	Tiny island country in Micronesia.	country.nru.desc	https://example.com/img/nr.jpg	https://upload.wikimedia.org/wikipedia/commons/3/30/Flag_of_Nauru.svg	1	2025-05-24	\N	7
519	NC	New Caledonia	territory.ncl.name	Special collectivity of France.	territory.ncl.desc	https://example.com/img/nc.jpg	https://upload.wikimedia.org/wikipedia/commons/2/23/Flag_of_New_Caledonia.svg	1	2025-05-24	\N	7
520	PF	French Polynesia	territory.pyf.name	Overseas collectivity of France.	territory.pyf.desc	https://example.com/img/pf.jpg	https://upload.wikimedia.org/wikipedia/commons/d/db/Flag_of_French_Polynesia.svg	1	2025-05-24	\N	7
383	MY	Malaysia	country.mys.name	A country in Southeast Asia.	country.mys.desc	https://example.com/img/my.jpg	https://upload.wikimedia.org/wikipedia/commons/6/66/Flag_of_Malaysia.svg	1	2025-05-22	2025-05-26	1
385	MN	Mongolia	country.mng.name	A country in East Asia.	country.mng.desc	https://example.com/img/mn.jpg	https://upload.wikimedia.org/wikipedia/commons/4/4c/Flag_of_Mongolia.svg	1	2025-05-22	2025-05-26	1
386	MM	Myanmar	country.mmr.name	A country in Southeast Asia.	country.mmr.desc	https://example.com/img/mm.jpg	https://upload.wikimedia.org/wikipedia/commons/8/8c/Flag_of_Myanmar.svg	1	2025-05-22	2025-05-26	1
387	NP	Nepal	country.npl.name	A country in South Asia.	country.npl.desc	https://example.com/img/np.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg	1	2025-05-22	2025-05-26	1
388	KP	North Korea (DPRK)	country.prk.name	A country in East Asia.	country.prk.desc	https://example.com/img/kp.jpg	https://upload.wikimedia.org/wikipedia/commons/5/51/Flag_of_North_Korea.svg	1	2025-05-22	2025-05-26	1
389	OM	Oman	country.omn.name	A country in Western Asia.	country.omn.desc	https://example.com/img/om.jpg	https://upload.wikimedia.org/wikipedia/commons/d/dd/Flag_of_Oman.svg	1	2025-05-22	2025-05-26	1
521	AS	American Samoa	territory.asm.name	Unincorporated territory of the United States.	territory.asm.desc	https://example.com/img/as.jpg	https://upload.wikimedia.org/wikipedia/commons/8/87/Flag_of_American_Samoa.svg	1	2025-05-24	\N	7
522	GU	Guam	territory.gum.name	Unincorporated territory of the United States.	territory.gum.desc	https://example.com/img/gu.jpg	https://upload.wikimedia.org/wikipedia/commons/0/07/Flag_of_Guam.svg	1	2025-05-24	\N	7
523	MP	Northern Mariana Islands	territory.mnp.name	Commonwealth of the United States.	territory.mnp.desc	https://example.com/img/mp.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e0/Flag_of_the_Northern_Mariana_Islands.svg	1	2025-05-24	\N	7
524	CK	Cook Islands	territory.cok.name	Self-governing island country in free association with New Zealand.	territory.cok.desc	https://example.com/img/ck.jpg	https://upload.wikimedia.org/wikipedia/commons/3/35/Flag_of_the_Cook_Islands.svg	1	2025-05-24	\N	7
525	NU	Niue	territory.niu.name	Island country in free association with New Zealand.	territory.niu.desc	https://example.com/img/nu.jpg	https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Niue.svg	1	2025-05-24	\N	7
526	TK	Tokelau	territory.tkl.name	Dependent territory of New Zealand.	territory.tkl.desc	https://example.com/img/tk.jpg	https://upload.wikimedia.org/wikipedia/commons/8/8e/Flag_of_Tokelau.svg	1	2025-05-24	\N	7
527	WF	Wallis and Futuna	territory.wlf.name	French island collectivity.	territory.wlf.desc	https://example.com/img/wf.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d2/Flag_of_Wallis_and_Futuna.svg	1	2025-05-24	\N	7
390	PK	Pakistan	country.pak.name	A country in South Asia.	country.pak.desc	https://example.com/img/pk.jpg	https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg	1	2025-05-22	2025-05-26	1
391	PS	Palestine, State of	country.pse.name	A state in the Middle East.	country.pse.desc	https://example.com/img/ps.jpg	https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg	1	2025-05-22	2025-05-26	1
392	PH	Philippines	country.phl.name	An archipelagic country in Southeast Asia.	country.phl.desc	https://example.com/img/ph.jpg	https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_the_Philippines.svg	1	2025-05-22	2025-05-26	1
393	QA	Qatar	country.qat.name	A country in Western Asia.	country.qat.desc	https://example.com/img/qa.jpg	https://upload.wikimedia.org/wikipedia/commons/6/65/Flag_of_Qatar.svg	1	2025-05-22	2025-05-26	1
394	SA	Saudi Arabia	country.sau.name	A kingdom in Western Asia.	country.sau.desc	https://example.com/img/sa.jpg	https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg	1	2025-05-22	2025-05-26	1
395	SG	Singapore	country.sgp.name	An island city-state in Southeast Asia.	country.sgp.desc	https://example.com/img/sg.jpg	https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Singapore.svg	1	2025-05-22	2025-05-26	1
396	KR	South Korea (ROK)	country.kor.name	A country in East Asia.	country.kor.desc	https://example.com/img/kr.jpg	https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg	1	2025-05-22	2025-05-26	1
397	LK	Sri Lanka	country.lka.name	An island country in South Asia.	country.lka.desc	https://example.com/img/lk.jpg	https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Sri_Lanka.svg	1	2025-05-22	2025-05-26	1
398	SY	Syria	country.syr.name	A country in Western Asia.	country.syr.desc	https://example.com/img/sy.jpg	https://upload.wikimedia.org/wikipedia/commons/5/53/Flag_of_Syria.svg	1	2025-05-22	2025-05-26	1
399	TW	Taiwan	country.twn.name	An island in East Asia.	country.twn.desc	https://example.com/img/tw.jpg	https://upload.wikimedia.org/wikipedia/commons/7/72/Flag_of_the_Republic_of_China.svg	1	2025-05-22	2025-05-26	1
400	TJ	Tajikistan	country.tjk.name	A country in Central Asia.	country.tjk.desc	https://example.com/img/tj.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d0/Flag_of_Tajikistan.svg	1	2025-05-22	2025-05-26	1
401	TH	Thailand	country.tha.name	A country in Southeast Asia.	country.tha.desc	https://example.com/img/th.jpg	https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_of_Thailand.svg	1	2025-05-22	2025-05-26	1
402	TL	Timor-Leste	country.tls.name	A country in Southeast Asia.	country.tls.desc	https://example.com/img/tl.jpg	https://upload.wikimedia.org/wikipedia/commons/2/26/Flag_of_East_Timor.svg	1	2025-05-22	2025-05-26	1
403	TR	Turkey	country.tur.name	A transcontinental country.	country.tur.desc	https://example.com/img/tr.jpg	https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Turkey.svg	1	2025-05-22	2025-05-26	1
404	TM	Turkmenistan	country.tkm.name	A country in Central Asia.	country.tkm.desc	https://example.com/img/tm.jpg	https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_Turkmenistan.svg	1	2025-05-22	2025-05-26	1
405	AE	United Arab Emirates	country.are.name	A country in Western Asia.	country.are.desc	https://example.com/img/ae.jpg	https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg	1	2025-05-22	2025-05-26	1
406	UZ	Uzbekistan	country.uzb.name	A country in Central Asia.	country.uzb.desc	https://example.com/img/uz.jpg	https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Uzbekistan.svg	1	2025-05-22	2025-05-26	1
407	YE	Yemen	country.yem.name	A country in Western Asia.	country.yem.desc	https://example.com/img/ye.jpg	https://upload.wikimedia.org/wikipedia/commons/8/89/Flag_of_Yemen.svg	1	2025-05-22	2025-05-26	1
549	EE	Estonia	country.est.name	A country in Northern Europe.	country.est.desc	https://example.com/img/ee.jpg	https://upload.wikimedia.org/wikipedia/commons/8/8f/Flag_of_Estonia.svg	1	2025-05-24	2025-05-26	2
551	FR	France	country.fra.name	A country in Western Europe.	country.fra.desc	https://example.com/img/fr.jpg	https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg	1	2025-05-24	2025-05-26	2
552	DE	Germany	country.deu.name	A country in Central Europe.	country.deu.desc	https://example.com/img/de.jpg	https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg	1	2025-05-24	2025-05-26	2
553	GR	Greece	country.grc.name	A country in Southeast Europe.	country.grc.desc	https://example.com/img/gr.jpg	https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Greece.svg	1	2025-05-24	2025-05-26	2
554	HU	Hungary	country.hun.name	A country in Central Europe.	country.hun.desc	https://example.com/img/hu.jpg	https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg	1	2025-05-24	2025-05-26	2
555	IS	Iceland	country.isl.name	A Nordic island country in the North Atlantic.	country.isl.desc	https://example.com/img/is.jpg	https://upload.wikimedia.org/wikipedia/commons/c/ce/Flag_of_Iceland.svg	1	2025-05-24	2025-05-26	2
556	IE	Ireland	country.irl.name	An island in Northwestern Europe.	country.irl.desc	https://example.com/img/ie.jpg	https://upload.wikimedia.org/wikipedia/commons/4/45/Flag_of_Ireland.svg	1	2025-05-24	2025-05-26	2
539	AL	Albania	country.alb.name	A country in Southeast Europe.	country.alb.desc	https://example.com/img/al.jpg	https://upload.wikimedia.org/wikipedia/commons/3/36/Flag_of_Albania.svg	1	2025-05-24	2025-05-26	2
540	AD	Andorra	country.and.name	A microstate in Southwestern Europe.	country.and.desc	https://example.com/img/ad.jpg	https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Andorra.svg	1	2025-05-24	2025-05-26	2
545	BG	Bulgaria	country.bgr.name	A country in Southeast Europe.	country.bgr.desc	https://example.com/img/bg.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Bulgaria.svg	1	2025-05-24	2025-05-26	2
546	HR	Croatia	country.hrv.name	A country at the crossroads of Central and Southeast Europe.	country.hrv.desc	https://example.com/img/hr.jpg	https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_Croatia.svg	1	2025-05-24	2025-05-26	2
547	CZ	Czech Republic	country.cze.name	A country in Central Europe.	country.cze.desc	https://example.com/img/cz.jpg	https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_Czech_Republic.svg	1	2025-05-24	2025-05-26	2
548	DK	Denmark	country.dnk.name	A Nordic country in Northern Europe.	country.dnk.desc	https://example.com/img/dk.jpg	https://upload.wikimedia.org/wikipedia/commons/9/9c/Flag_of_Denmark.svg	1	2025-05-24	2025-05-26	2
550	FI	Finland	country.fin.name	A Nordic country in Northern Europe.	country.fin.desc	https://example.com/img/fi.jpg	https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Finland.svg	1	2025-05-24	2025-05-26	2
557	IT	Italy	country.ita.name	A country in Southern Europe.	country.ita.desc	https://example.com/img/it.jpg	https://upload.wikimedia.org/wikipedia/en/0/03/Flag_of_Italy.svg	1	2025-05-24	2025-05-26	2
558	XK	Kosovo	country.rks.name	A partially recognised state in Southeast Europe.	country.rks.desc	https://example.com/img/xk.jpg	https://upload.wikimedia.org/wikipedia/commons/1/1f/Flag_of_Kosovo.svg	1	2025-05-24	2025-05-26	2
559	LV	Latvia	country.lva.name	A country in Northern Europe.	country.lva.desc	https://example.com/img/lv.jpg	https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Latvia.svg	1	2025-05-24	2025-05-26	2
560	LI	Liechtenstein	country.lie.name	A microstate in Central Europe.	country.lie.desc	https://example.com/img/li.jpg	https://upload.wikimedia.org/wikipedia/commons/4/47/Flag_of_Liechtenstein.svg	1	2025-05-24	2025-05-26	2
561	LT	Lithuania	country.ltu.name	A country in Northern Europe.	country.ltu.desc	https://example.com/img/lt.jpg	https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Lithuania.svg	1	2025-05-24	2025-05-26	2
562	LU	Luxembourg	country.lux.name	A country in Western Europe.	country.lux.desc	https://example.com/img/lu.jpg	https://upload.wikimedia.org/wikipedia/commons/d/da/Flag_of_Luxembourg.svg	1	2025-05-24	2025-05-26	2
563	MT	Malta	country.mlt.name	An island country in Southern Europe.	country.mlt.desc	https://example.com/img/mt.jpg	https://upload.wikimedia.org/wikipedia/commons/7/73/Flag_of_Malta.svg	1	2025-05-24	2025-05-26	2
564	MD	Moldova	country.mda.name	A country in Eastern Europe.	country.mda.desc	https://example.com/img/md.jpg	https://upload.wikimedia.org/wikipedia/commons/2/27/Flag_of_Moldova.svg	1	2025-05-24	2025-05-26	2
565	MC	Monaco	country.mco.name	A microstate on the French Riviera.	country.mco.desc	https://example.com/img/mc.jpg	https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_of_Monaco.svg	1	2025-05-24	2025-05-26	2
566	ME	Montenegro	country.mne.name	A country in Southeast Europe.	country.mne.desc	https://example.com/img/me.jpg	https://upload.wikimedia.org/wikipedia/commons/6/64/Flag_of_Montenegro.svg	1	2025-05-24	2025-05-26	2
567	NL	Netherlands	country.nld.name	A country in Western Europe.	country.nld.desc	https://example.com/img/nl.jpg	https://upload.wikimedia.org/wikipedia/commons/2/20/Flag_of_the_Netherlands.svg	1	2025-05-24	2025-05-26	2
568	MK	North Macedonia	country.mkd.name	A country in Southeast Europe.	country.mkd.desc	https://example.com/img/mk.jpg	https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_of_North_Macedonia.svg	1	2025-05-24	2025-05-26	2
569	NO	Norway	country.nor.name	A Nordic country in Northern Europe.	country.nor.desc	https://example.com/img/no.jpg	https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg	1	2025-05-24	2025-05-26	2
570	PL	Poland	country.pol.name	A country in Central Europe.	country.pol.desc	https://example.com/img/pl.jpg	https://upload.wikimedia.org/wikipedia/en/1/12/Flag_of_Poland.svg	1	2025-05-24	2025-05-26	2
571	PT	Portugal	country.prt.name	A country in Southwestern Europe.	country.prt.desc	https://example.com/img/pt.jpg	https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Portugal.svg	1	2025-05-24	2025-05-26	2
572	RO	Romania	country.rou.name	A country in Southeast Europe.	country.rou.desc	https://example.com/img/ro.jpg	https://upload.wikimedia.org/wikipedia/commons/7/73/Flag_of_Romania.svg	1	2025-05-24	2025-05-26	2
573	RU	Russia	country.rus.name	A transcontinental country in Eastern Europe and Northern Asia.	country.rus.desc	https://example.com/img/ru.jpg	https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg	1	2025-05-24	2025-05-26	2
574	SM	San Marino	country.smr.name	A microstate surrounded by Italy.	country.smr.desc	https://example.com/img/sm.jpg	https://upload.wikimedia.org/wikipedia/commons/b/b1/Flag_of_San_Marino.svg	1	2025-05-24	2025-05-26	2
575	RS	Serbia	country.srb.name	A country in Southeast Europe.	country.srb.desc	https://example.com/img/rs.jpg	https://upload.wikimedia.org/wikipedia/commons/f/ff/Flag_of_Serbia.svg	1	2025-05-24	2025-05-26	2
576	SK	Slovakia	country.svk.name	A country in Central Europe.	country.svk.desc	https://example.com/img/sk.jpg	https://upload.wikimedia.org/wikipedia/commons/e/e6/Flag_of_Slovakia.svg	1	2025-05-24	2025-05-26	2
577	SI	Slovenia	country.svn.name	A country in Central Europe.	country.svn.desc	https://example.com/img/si.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f0/Flag_of_Slovenia.svg	1	2025-05-24	2025-05-26	2
578	ES	Spain	country.esp.name	A country in Southwestern Europe.	country.esp.desc	https://example.com/img/es.jpg	https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg	1	2025-05-24	2025-05-26	2
579	SE	Sweden	country.swe.name	A Nordic country in Northern Europe.	country.swe.desc	https://example.com/img/se.jpg	https://upload.wikimedia.org/wikipedia/en/4/4c/Flag_of_Sweden.svg	1	2025-05-24	2025-05-26	2
581	UA	Ukraine	country.ukr.name	A country in Eastern Europe.	country.ukr.desc	https://example.com/img/ua.jpg	https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Ukraine.svg	1	2025-05-24	2025-05-26	2
582	GB	United Kingdom	country.gbr.name	An island country in Northwestern Europe.	country.gbr.desc	https://example.com/img/gb.jpg	https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg	1	2025-05-24	2025-05-26	2
583	VA	Vatican City	country.vat.name	A city-state surrounded by Rome, Italy.	country.vat.desc	https://example.com/img/va.jpg	https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_the_Vatican_City.svg	1	2025-05-24	2025-05-26	2
580	CH	Switzerland	country.che.name	A country in Central Europe.	country.che.desc	https://example.com/img/ch.jpg	https://upload.wikimedia.org/wikipedia/commons/f/f3/Flag_of_Switzerland.svg	1	2025-05-24	2025-05-26	2
\.


--
-- Data for Name: regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.regions (id, name, code, name_code, description, description_code, background_image, logo, status, created_date, updated_date, country_id) FROM stdin;
64	Thành phố Hà Nội	01	region.ha_noi	\N	\N	\N	\N	1	2025-05-25	\N	2
65	Tỉnh Hà Giang	02	region.ha_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
66	Tỉnh Cao Bằng	04	region.cao_bang	\N	\N	\N	\N	1	2025-05-25	\N	2
67	Tỉnh Bắc Kạn	06	region.bac_kan	\N	\N	\N	\N	1	2025-05-25	\N	2
68	Tỉnh Tuyên Quang	08	region.tuyen_quang	\N	\N	\N	\N	1	2025-05-25	\N	2
69	Tỉnh Lào Cai	10	region.lao_cai	\N	\N	\N	\N	1	2025-05-25	\N	2
70	Tỉnh Điện Biên	11	region.dien_bien	\N	\N	\N	\N	1	2025-05-25	\N	2
71	Tỉnh Lai Châu	12	region.lai_chau	\N	\N	\N	\N	1	2025-05-25	\N	2
72	Tỉnh Sơn La	14	region.son_la	\N	\N	\N	\N	1	2025-05-25	\N	2
73	Tỉnh Yên Bái	15	region.yen_bai	\N	\N	\N	\N	1	2025-05-25	\N	2
74	Tỉnh Hòa Bình	17	region.hoa_binh	\N	\N	\N	\N	1	2025-05-25	\N	2
75	Tỉnh Thái Nguyên	19	region.thai_nguyen	\N	\N	\N	\N	1	2025-05-25	\N	2
76	Tỉnh Lạng Sơn	20	region.lang_son	\N	\N	\N	\N	1	2025-05-25	\N	2
77	Tỉnh Quảng Ninh	22	region.quang_ninh	\N	\N	\N	\N	1	2025-05-25	\N	2
78	Tỉnh Bắc Giang	24	region.bac_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
79	Tỉnh Phú Thọ	25	region.phu_tho	\N	\N	\N	\N	1	2025-05-25	\N	2
80	Tỉnh Vĩnh Phúc	26	region.vinh_phuc	\N	\N	\N	\N	1	2025-05-25	\N	2
81	Tỉnh Bắc Ninh	27	region.bac_ninh	\N	\N	\N	\N	1	2025-05-25	\N	2
82	Tỉnh Hải Dương	30	region.hai_duong	\N	\N	\N	\N	1	2025-05-25	\N	2
83	Thành phố Hải Phòng	31	region.hai_phong	\N	\N	\N	\N	1	2025-05-25	\N	2
84	Tỉnh Hưng Yên	33	region.hung_yen	\N	\N	\N	\N	1	2025-05-25	\N	2
85	Tỉnh Thái Bình	34	region.thai_binh	\N	\N	\N	\N	1	2025-05-25	\N	2
86	Tỉnh Hà Nam	35	region.ha_nam	\N	\N	\N	\N	1	2025-05-25	\N	2
87	Tỉnh Nam Định	36	region.nam_dinh	\N	\N	\N	\N	1	2025-05-25	\N	2
88	Tỉnh Ninh Bình	37	region.ninh_binh	\N	\N	\N	\N	1	2025-05-25	\N	2
89	Tỉnh Thanh Hóa	38	region.thanh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	2
90	Tỉnh Nghệ An	40	region.nghe_an	\N	\N	\N	\N	1	2025-05-25	\N	2
91	Tỉnh Hà Tĩnh	42	region.ha_tinh	\N	\N	\N	\N	1	2025-05-25	\N	2
92	Tỉnh Quảng Bình	44	region.quang_binh	\N	\N	\N	\N	1	2025-05-25	\N	2
93	Tỉnh Quảng Trị	45	region.quang_tri	\N	\N	\N	\N	1	2025-05-25	\N	2
94	Tỉnh Thừa Thiên Huế	46	region.thua_thien_hue	\N	\N	\N	\N	1	2025-05-25	\N	2
95	Thành phố Đà Nẵng	48	region.da_nang	\N	\N	\N	\N	1	2025-05-25	\N	2
96	Tỉnh Quảng Nam	49	region.quang_nam	\N	\N	\N	\N	1	2025-05-25	\N	2
97	Tỉnh Quảng Ngãi	51	region.quang_ngai	\N	\N	\N	\N	1	2025-05-25	\N	2
98	Tỉnh Bình Định	52	region.binh_dinh	\N	\N	\N	\N	1	2025-05-25	\N	2
99	Tỉnh Phú Yên	54	region.phu_yen	\N	\N	\N	\N	1	2025-05-25	\N	2
100	Tỉnh Khánh Hòa	56	region.khanh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	2
101	Tỉnh Ninh Thuận	58	region.ninh_thuan	\N	\N	\N	\N	1	2025-05-25	\N	2
102	Tỉnh Bình Thuận	60	region.binh_thuan	\N	\N	\N	\N	1	2025-05-25	\N	2
103	Tỉnh Kon Tum	62	region.kon_tum	\N	\N	\N	\N	1	2025-05-25	\N	2
104	Tỉnh Gia Lai	64	region.gia_lai	\N	\N	\N	\N	1	2025-05-25	\N	2
105	Tỉnh Đắk Lắk	66	region.dak_lak	\N	\N	\N	\N	1	2025-05-25	\N	2
106	Tỉnh Đắk Nông	67	region.dak_nong	\N	\N	\N	\N	1	2025-05-25	\N	2
107	Tỉnh Lâm Đồng	68	region.lam_dong	\N	\N	\N	\N	1	2025-05-25	\N	2
108	Tỉnh Bình Phước	70	region.binh_phuoc	\N	\N	\N	\N	1	2025-05-25	\N	2
109	Tỉnh Tây Ninh	72	region.tay_ninh	\N	\N	\N	\N	1	2025-05-25	\N	2
110	Tỉnh Bình Dương	74	region.binh_duong	\N	\N	\N	\N	1	2025-05-25	\N	2
111	Tỉnh Đồng Nai	75	region.dong_nai	\N	\N	\N	\N	1	2025-05-25	\N	2
112	Tỉnh Bà Rịa - Vũng Tàu	77	region.ba_ria_vung_tau	\N	\N	\N	\N	1	2025-05-25	\N	2
113	Thành phố Hồ Chí Minh	79	region.ho_chi_minh	\N	\N	\N	\N	1	2025-05-25	\N	2
114	Tỉnh Long An	80	region.long_an	\N	\N	\N	\N	1	2025-05-25	\N	2
115	Tỉnh Tiền Giang	82	region.tien_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
116	Tỉnh Bến Tre	83	region.ben_tre	\N	\N	\N	\N	1	2025-05-25	\N	2
117	Tỉnh Trà Vinh	84	region.tra_vinh	\N	\N	\N	\N	1	2025-05-25	\N	2
118	Tỉnh Vĩnh Long	86	region.vinh_long	\N	\N	\N	\N	1	2025-05-25	\N	2
119	Tỉnh Đồng Tháp	87	region.dong_thap	\N	\N	\N	\N	1	2025-05-25	\N	2
120	Tỉnh An Giang	89	region.an_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
121	Tỉnh Kiên Giang	91	region.kien_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
122	Thành phố Cần Thơ	92	region.can_tho	\N	\N	\N	\N	1	2025-05-25	\N	2
123	Tỉnh Hậu Giang	93	region.hau_giang	\N	\N	\N	\N	1	2025-05-25	\N	2
124	Tỉnh Sóc Trăng	94	region.soc_trang	\N	\N	\N	\N	1	2025-05-25	\N	2
125	Tỉnh Bạc Liêu	95	region.bac_lieu	\N	\N	\N	\N	1	2025-05-25	\N	2
126	Tỉnh Cà Mau	96	region.ca_mau	\N	\N	\N	\N	1	2025-05-25	\N	2
\.


--
-- Data for Name: districts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.districts (id, name, code, name_code, description, description_code, background_image, logo, status, created_date, updated_date, region_id) FROM stdin;
1	Quận Ba Đình	001	district.ba_dinh	\N	\N	\N	\N	1	2025-05-25	\N	64
2	Quận Hoàn Kiếm	002	district.hoan_kiem	\N	\N	\N	\N	1	2025-05-25	\N	64
3	Quận Tây Hồ	003	district.tay_ho	\N	\N	\N	\N	1	2025-05-25	\N	64
4	Quận Long Biên	004	district.long_bien	\N	\N	\N	\N	1	2025-05-25	\N	64
5	Quận Cầu Giấy	005	district.cau_giay	\N	\N	\N	\N	1	2025-05-25	\N	64
6	Quận Đống Đa	006	district.dong_da	\N	\N	\N	\N	1	2025-05-25	\N	64
7	Quận Hai Bà Trưng	007	district.hai_ba_trung	\N	\N	\N	\N	1	2025-05-25	\N	64
8	Quận Hoàng Mai	008	district.hoang_mai	\N	\N	\N	\N	1	2025-05-25	\N	64
9	Quận Thanh Xuân	009	district.thanh_xuan	\N	\N	\N	\N	1	2025-05-25	\N	64
10	Huyện Sóc Sơn	016	district.soc_son	\N	\N	\N	\N	1	2025-05-25	\N	64
11	Huyện Đông Anh	017	district.dong_anh	\N	\N	\N	\N	1	2025-05-25	\N	64
12	Huyện Gia Lâm	018	district.gia_lam	\N	\N	\N	\N	1	2025-05-25	\N	64
13	Quận Nam Từ Liêm	019	district.nam_tu_liem	\N	\N	\N	\N	1	2025-05-25	\N	64
14	Huyện Thanh Trì	020	district.thanh_tri	\N	\N	\N	\N	1	2025-05-25	\N	64
15	Quận Bắc Từ Liêm	021	district.bac_tu_liem	\N	\N	\N	\N	1	2025-05-25	\N	64
16	Huyện Mê Linh	250	district.me_linh	\N	\N	\N	\N	1	2025-05-25	\N	64
17	Quận Hà Đông	268	district.ha_dong	\N	\N	\N	\N	1	2025-05-25	\N	64
18	Thị xã Sơn Tây	269	district.son_tay	\N	\N	\N	\N	1	2025-05-25	\N	64
19	Huyện Ba Vì	271	district.ba_vi	\N	\N	\N	\N	1	2025-05-25	\N	64
20	Huyện Phúc Thọ	272	district.phuc_tho	\N	\N	\N	\N	1	2025-05-25	\N	64
21	Huyện Đan Phượng	273	district.dan_phuong	\N	\N	\N	\N	1	2025-05-25	\N	64
22	Huyện Hoài Đức	274	district.hoai_duc	\N	\N	\N	\N	1	2025-05-25	\N	64
23	Huyện Quốc Oai	275	district.quoc_oai	\N	\N	\N	\N	1	2025-05-25	\N	64
24	Huyện Thạch Thất	276	district.thach_that	\N	\N	\N	\N	1	2025-05-25	\N	64
25	Huyện Chương Mỹ	277	district.chuong_my	\N	\N	\N	\N	1	2025-05-25	\N	64
26	Huyện Thanh Oai	278	district.thanh_oai	\N	\N	\N	\N	1	2025-05-25	\N	64
27	Huyện Thường Tín	279	district.thuong_tin	\N	\N	\N	\N	1	2025-05-25	\N	64
28	Huyện Phú Xuyên	280	district.phu_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	64
29	Huyện Ứng Hòa	281	district.ung_hoa	\N	\N	\N	\N	1	2025-05-25	\N	64
30	Huyện Mỹ Đức	282	district.my_duc	\N	\N	\N	\N	1	2025-05-25	\N	64
31	Thành phố Hà Giang	024	district.ha_giang	\N	\N	\N	\N	1	2025-05-25	\N	65
32	Huyện Đồng Văn	026	district.dong_van	\N	\N	\N	\N	1	2025-05-25	\N	65
33	Huyện Mèo Vạc	027	district.meo_vac	\N	\N	\N	\N	1	2025-05-25	\N	65
34	Huyện Yên Minh	028	district.yen_minh	\N	\N	\N	\N	1	2025-05-25	\N	65
35	Huyện Quản Bạ	029	district.quan_ba	\N	\N	\N	\N	1	2025-05-25	\N	65
36	Huyện Vị Xuyên	030	district.vi_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	65
37	Huyện Bắc Mê	031	district.bac_me	\N	\N	\N	\N	1	2025-05-25	\N	65
38	Huyện Hoàng Su Phì	032	district.hoang_su_phi	\N	\N	\N	\N	1	2025-05-25	\N	65
39	Huyện Xín Mần	033	district.xin_man	\N	\N	\N	\N	1	2025-05-25	\N	65
40	Huyện Bắc Quang	034	district.bac_quang	\N	\N	\N	\N	1	2025-05-25	\N	65
41	Huyện Quang Bình	035	district.quang_binh	\N	\N	\N	\N	1	2025-05-25	\N	65
42	Thành phố Cao Bằng	040	district.cao_bang	\N	\N	\N	\N	1	2025-05-25	\N	66
43	Huyện Bảo Lạc	042	district.bao_lac	\N	\N	\N	\N	1	2025-05-25	\N	66
44	Huyện Bảo Lâm	043	district.bao_lam	\N	\N	\N	\N	1	2025-05-25	\N	66
45	Huyện Hà Quảng	045	district.ha_quang	\N	\N	\N	\N	1	2025-05-25	\N	66
46	Huyện Trùng Khánh	047	district.trung_khanh	\N	\N	\N	\N	1	2025-05-25	\N	66
47	Huyện Hạ Lang	048	district.ha_lang	\N	\N	\N	\N	1	2025-05-25	\N	66
48	Huyện Quảng Hòa	049	district.quang_hoa	\N	\N	\N	\N	1	2025-05-25	\N	66
49	Huyện Hoà An	050	district.hoa_an	\N	\N	\N	\N	1	2025-05-25	\N	66
50	Huyện Nguyên Bình	051	district.nguyen_binh	\N	\N	\N	\N	1	2025-05-25	\N	66
51	Huyện Thạch An	052	district.thach_an	\N	\N	\N	\N	1	2025-05-25	\N	66
52	Thành phố Bắc Kạn	058	district.bac_kan	\N	\N	\N	\N	1	2025-05-25	\N	67
53	Huyện Pác Nặm	060	district.pac_nam	\N	\N	\N	\N	1	2025-05-25	\N	67
54	Huyện Ba Bể	061	district.ba_be	\N	\N	\N	\N	1	2025-05-25	\N	67
55	Huyện Ngân Sơn	062	district.ngan_son	\N	\N	\N	\N	1	2025-05-25	\N	67
56	Huyện Bạch Thông	063	district.bach_thong	\N	\N	\N	\N	1	2025-05-25	\N	67
57	Huyện Chợ Đồn	064	district.cho_don	\N	\N	\N	\N	1	2025-05-25	\N	67
58	Huyện Chợ Mới	065	district.cho_moi	\N	\N	\N	\N	1	2025-05-25	\N	67
59	Huyện Na Rì	066	district.na_ri	\N	\N	\N	\N	1	2025-05-25	\N	67
60	Thành phố Tuyên Quang	070	district.tuyen_quang	\N	\N	\N	\N	1	2025-05-25	\N	68
61	Huyện Lâm Bình	072	district.lam_binh	\N	\N	\N	\N	1	2025-05-25	\N	68
62	Huyện Na Hang	073	district.na_hang	\N	\N	\N	\N	1	2025-05-25	\N	68
63	Huyện Chiêm Hóa	074	district.chiem_hoa	\N	\N	\N	\N	1	2025-05-25	\N	68
64	Huyện Hàm Yên	075	district.ham_yen	\N	\N	\N	\N	1	2025-05-25	\N	68
65	Huyện Yên Sơn	076	district.yen_son	\N	\N	\N	\N	1	2025-05-25	\N	68
66	Huyện Sơn Dương	077	district.son_duong	\N	\N	\N	\N	1	2025-05-25	\N	68
67	Thành phố Lào Cai	080	district.lao_cai	\N	\N	\N	\N	1	2025-05-25	\N	69
68	Huyện Bát Xát	082	district.bat_xat	\N	\N	\N	\N	1	2025-05-25	\N	69
69	Huyện Mường Khương	083	district.muong_khuong	\N	\N	\N	\N	1	2025-05-25	\N	69
70	Huyện Si Ma Cai	084	district.si_ma_cai	\N	\N	\N	\N	1	2025-05-25	\N	69
71	Huyện Bắc Hà	085	district.bac_ha	\N	\N	\N	\N	1	2025-05-25	\N	69
72	Huyện Bảo Thắng	086	district.bao_thang	\N	\N	\N	\N	1	2025-05-25	\N	69
73	Huyện Bảo Yên	087	district.bao_yen	\N	\N	\N	\N	1	2025-05-25	\N	69
74	Thị xã Sa Pa	088	district.sa_pa	\N	\N	\N	\N	1	2025-05-25	\N	69
75	Huyện Văn Bàn	089	district.van_ban	\N	\N	\N	\N	1	2025-05-25	\N	69
76	Thành phố Điện Biên Phủ	094	district.dien_bien_phu	\N	\N	\N	\N	1	2025-05-25	\N	70
77	Thị xã Mường Lay	095	district.muong_lay	\N	\N	\N	\N	1	2025-05-25	\N	70
78	Huyện Mường Nhé	096	district.muong_nhe	\N	\N	\N	\N	1	2025-05-25	\N	70
79	Huyện Mường Chà	097	district.muong_cha	\N	\N	\N	\N	1	2025-05-25	\N	70
80	Huyện Tủa Chùa	098	district.tua_chua	\N	\N	\N	\N	1	2025-05-25	\N	70
81	Huyện Tuần Giáo	099	district.tuan_giao	\N	\N	\N	\N	1	2025-05-25	\N	70
82	Huyện Điện Biên	100	district.dien_bien	\N	\N	\N	\N	1	2025-05-25	\N	70
83	Huyện Điện Biên Đông	101	district.dien_bien_dong	\N	\N	\N	\N	1	2025-05-25	\N	70
84	Huyện Mường Ảng	102	district.muong_ang	\N	\N	\N	\N	1	2025-05-25	\N	70
85	Huyện Nậm Pồ	103	district.nam_po	\N	\N	\N	\N	1	2025-05-25	\N	70
86	Thành phố Lai Châu	105	district.lai_chau	\N	\N	\N	\N	1	2025-05-25	\N	71
87	Huyện Tam Đường	106	district.tam_duong	\N	\N	\N	\N	1	2025-05-25	\N	71
88	Huyện Mường Tè	107	district.muong_te	\N	\N	\N	\N	1	2025-05-25	\N	71
89	Huyện Sìn Hồ	108	district.sin_ho	\N	\N	\N	\N	1	2025-05-25	\N	71
90	Huyện Phong Thổ	109	district.phong_tho	\N	\N	\N	\N	1	2025-05-25	\N	71
91	Huyện Than Uyên	110	district.than_uyen	\N	\N	\N	\N	1	2025-05-25	\N	71
92	Huyện Tân Uyên	111	district.tan_uyen	\N	\N	\N	\N	1	2025-05-25	\N	71
93	Huyện Nậm Nhùn	112	district.nam_nhun	\N	\N	\N	\N	1	2025-05-25	\N	71
94	Thành phố Sơn La	116	district.son_la	\N	\N	\N	\N	1	2025-05-25	\N	72
95	Huyện Quỳnh Nhai	118	district.quynh_nhai	\N	\N	\N	\N	1	2025-05-25	\N	72
96	Huyện Thuận Châu	119	district.thuan_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
97	Huyện Mường La	120	district.muong_la	\N	\N	\N	\N	1	2025-05-25	\N	72
98	Huyện Bắc Yên	121	district.bac_yen	\N	\N	\N	\N	1	2025-05-25	\N	72
99	Huyện Phù Yên	122	district.phu_yen	\N	\N	\N	\N	1	2025-05-25	\N	72
100	Huyện Mộc Châu	123	district.moc_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
101	Huyện Yên Châu	124	district.yen_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
102	Huyện Mai Sơn	125	district.mai_son	\N	\N	\N	\N	1	2025-05-25	\N	72
103	Huyện Sông Mã	126	district.song_ma	\N	\N	\N	\N	1	2025-05-25	\N	72
104	Huyện Sốp Cộp	127	district.sop_cop	\N	\N	\N	\N	1	2025-05-25	\N	72
105	Huyện Vân Hồ	128	district.van_ho	\N	\N	\N	\N	1	2025-05-25	\N	72
106	Thành phố Yên Bái	132	district.yen_bai	\N	\N	\N	\N	1	2025-05-25	\N	73
107	Thị xã Nghĩa Lộ	133	district.nghia_lo	\N	\N	\N	\N	1	2025-05-25	\N	73
108	Huyện Lục Yên	135	district.luc_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
109	Huyện Văn Yên	136	district.van_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
110	Huyện Mù Cang Chải	137	district.mu_cang_chai	\N	\N	\N	\N	1	2025-05-25	\N	73
111	Huyện Trấn Yên	138	district.tran_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
112	Huyện Trạm Tấu	139	district.tram_tau	\N	\N	\N	\N	1	2025-05-25	\N	73
113	Huyện Văn Chấn	140	district.van_chan	\N	\N	\N	\N	1	2025-05-25	\N	73
114	Huyện Yên Bình	141	district.yen_binh	\N	\N	\N	\N	1	2025-05-25	\N	73
115	Quận Ba Đình	001	district.ba_dinh	\N	\N	\N	\N	1	2025-05-25	\N	64
116	Quận Hoàn Kiếm	002	district.hoan_kiem	\N	\N	\N	\N	1	2025-05-25	\N	64
117	Quận Tây Hồ	003	district.tay_ho	\N	\N	\N	\N	1	2025-05-25	\N	64
118	Quận Long Biên	004	district.long_bien	\N	\N	\N	\N	1	2025-05-25	\N	64
119	Quận Cầu Giấy	005	district.cau_giay	\N	\N	\N	\N	1	2025-05-25	\N	64
120	Quận Đống Đa	006	district.dong_da	\N	\N	\N	\N	1	2025-05-25	\N	64
121	Quận Hai Bà Trưng	007	district.hai_ba_trung	\N	\N	\N	\N	1	2025-05-25	\N	64
122	Quận Hoàng Mai	008	district.hoang_mai	\N	\N	\N	\N	1	2025-05-25	\N	64
123	Quận Thanh Xuân	009	district.thanh_xuan	\N	\N	\N	\N	1	2025-05-25	\N	64
124	Huyện Sóc Sơn	016	district.soc_son	\N	\N	\N	\N	1	2025-05-25	\N	64
125	Huyện Đông Anh	017	district.dong_anh	\N	\N	\N	\N	1	2025-05-25	\N	64
126	Huyện Gia Lâm	018	district.gia_lam	\N	\N	\N	\N	1	2025-05-25	\N	64
127	Quận Nam Từ Liêm	019	district.nam_tu_liem	\N	\N	\N	\N	1	2025-05-25	\N	64
128	Huyện Thanh Trì	020	district.thanh_tri	\N	\N	\N	\N	1	2025-05-25	\N	64
129	Quận Bắc Từ Liêm	021	district.bac_tu_liem	\N	\N	\N	\N	1	2025-05-25	\N	64
130	Huyện Mê Linh	250	district.me_linh	\N	\N	\N	\N	1	2025-05-25	\N	64
131	Quận Hà Đông	268	district.ha_dong	\N	\N	\N	\N	1	2025-05-25	\N	64
132	Thị xã Sơn Tây	269	district.son_tay	\N	\N	\N	\N	1	2025-05-25	\N	64
133	Huyện Ba Vì	271	district.ba_vi	\N	\N	\N	\N	1	2025-05-25	\N	64
134	Huyện Phúc Thọ	272	district.phuc_tho	\N	\N	\N	\N	1	2025-05-25	\N	64
135	Huyện Đan Phượng	273	district.dan_phuong	\N	\N	\N	\N	1	2025-05-25	\N	64
136	Huyện Hoài Đức	274	district.hoai_duc	\N	\N	\N	\N	1	2025-05-25	\N	64
137	Huyện Quốc Oai	275	district.quoc_oai	\N	\N	\N	\N	1	2025-05-25	\N	64
138	Huyện Thạch Thất	276	district.thach_that	\N	\N	\N	\N	1	2025-05-25	\N	64
139	Huyện Chương Mỹ	277	district.chuong_my	\N	\N	\N	\N	1	2025-05-25	\N	64
140	Huyện Thanh Oai	278	district.thanh_oai	\N	\N	\N	\N	1	2025-05-25	\N	64
141	Huyện Thường Tín	279	district.thuong_tin	\N	\N	\N	\N	1	2025-05-25	\N	64
142	Huyện Phú Xuyên	280	district.phu_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	64
143	Huyện Ứng Hòa	281	district.ung_hoa	\N	\N	\N	\N	1	2025-05-25	\N	64
144	Huyện Mỹ Đức	282	district.my_duc	\N	\N	\N	\N	1	2025-05-25	\N	64
145	Thành phố Hà Giang	024	district.ha_giang	\N	\N	\N	\N	1	2025-05-25	\N	65
146	Huyện Đồng Văn	026	district.dong_van	\N	\N	\N	\N	1	2025-05-25	\N	65
147	Huyện Mèo Vạc	027	district.meo_vac	\N	\N	\N	\N	1	2025-05-25	\N	65
148	Huyện Yên Minh	028	district.yen_minh	\N	\N	\N	\N	1	2025-05-25	\N	65
149	Huyện Quản Bạ	029	district.quan_ba	\N	\N	\N	\N	1	2025-05-25	\N	65
150	Huyện Vị Xuyên	030	district.vi_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	65
151	Huyện Bắc Mê	031	district.bac_me	\N	\N	\N	\N	1	2025-05-25	\N	65
152	Huyện Hoàng Su Phì	032	district.hoang_su_phi	\N	\N	\N	\N	1	2025-05-25	\N	65
153	Huyện Xín Mần	033	district.xin_man	\N	\N	\N	\N	1	2025-05-25	\N	65
154	Huyện Bắc Quang	034	district.bac_quang	\N	\N	\N	\N	1	2025-05-25	\N	65
155	Huyện Quang Bình	035	district.quang_binh	\N	\N	\N	\N	1	2025-05-25	\N	65
156	Thành phố Cao Bằng	040	district.cao_bang	\N	\N	\N	\N	1	2025-05-25	\N	66
157	Huyện Bảo Lạc	042	district.bao_lac	\N	\N	\N	\N	1	2025-05-25	\N	66
158	Huyện Bảo Lâm	043	district.bao_lam	\N	\N	\N	\N	1	2025-05-25	\N	66
159	Huyện Hà Quảng	045	district.ha_quang	\N	\N	\N	\N	1	2025-05-25	\N	66
160	Huyện Trùng Khánh	047	district.trung_khanh	\N	\N	\N	\N	1	2025-05-25	\N	66
161	Huyện Hạ Lang	048	district.ha_lang	\N	\N	\N	\N	1	2025-05-25	\N	66
162	Huyện Quảng Hòa	049	district.quang_hoa	\N	\N	\N	\N	1	2025-05-25	\N	66
163	Huyện Hoà An	050	district.hoa_an	\N	\N	\N	\N	1	2025-05-25	\N	66
164	Huyện Nguyên Bình	051	district.nguyen_binh	\N	\N	\N	\N	1	2025-05-25	\N	66
165	Huyện Thạch An	052	district.thach_an	\N	\N	\N	\N	1	2025-05-25	\N	66
166	Thành phố Bắc Kạn	058	district.bac_kan	\N	\N	\N	\N	1	2025-05-25	\N	67
167	Huyện Pác Nặm	060	district.pac_nam	\N	\N	\N	\N	1	2025-05-25	\N	67
168	Huyện Ba Bể	061	district.ba_be	\N	\N	\N	\N	1	2025-05-25	\N	67
169	Huyện Ngân Sơn	062	district.ngan_son	\N	\N	\N	\N	1	2025-05-25	\N	67
170	Huyện Bạch Thông	063	district.bach_thong	\N	\N	\N	\N	1	2025-05-25	\N	67
171	Huyện Chợ Đồn	064	district.cho_don	\N	\N	\N	\N	1	2025-05-25	\N	67
172	Huyện Chợ Mới	065	district.cho_moi	\N	\N	\N	\N	1	2025-05-25	\N	67
173	Huyện Na Rì	066	district.na_ri	\N	\N	\N	\N	1	2025-05-25	\N	67
174	Thành phố Tuyên Quang	070	district.tuyen_quang	\N	\N	\N	\N	1	2025-05-25	\N	68
175	Huyện Lâm Bình	072	district.lam_binh	\N	\N	\N	\N	1	2025-05-25	\N	68
176	Huyện Na Hang	073	district.na_hang	\N	\N	\N	\N	1	2025-05-25	\N	68
177	Huyện Chiêm Hóa	074	district.chiem_hoa	\N	\N	\N	\N	1	2025-05-25	\N	68
178	Huyện Hàm Yên	075	district.ham_yen	\N	\N	\N	\N	1	2025-05-25	\N	68
179	Huyện Yên Sơn	076	district.yen_son	\N	\N	\N	\N	1	2025-05-25	\N	68
180	Huyện Sơn Dương	077	district.son_duong	\N	\N	\N	\N	1	2025-05-25	\N	68
181	Thành phố Lào Cai	080	district.lao_cai	\N	\N	\N	\N	1	2025-05-25	\N	69
182	Huyện Bát Xát	082	district.bat_xat	\N	\N	\N	\N	1	2025-05-25	\N	69
183	Huyện Mường Khương	083	district.muong_khuong	\N	\N	\N	\N	1	2025-05-25	\N	69
184	Huyện Si Ma Cai	084	district.si_ma_cai	\N	\N	\N	\N	1	2025-05-25	\N	69
185	Huyện Bắc Hà	085	district.bac_ha	\N	\N	\N	\N	1	2025-05-25	\N	69
186	Huyện Bảo Thắng	086	district.bao_thang	\N	\N	\N	\N	1	2025-05-25	\N	69
187	Huyện Bảo Yên	087	district.bao_yen	\N	\N	\N	\N	1	2025-05-25	\N	69
188	Thị xã Sa Pa	088	district.sa_pa	\N	\N	\N	\N	1	2025-05-25	\N	69
189	Huyện Văn Bàn	089	district.van_ban	\N	\N	\N	\N	1	2025-05-25	\N	69
190	Thành phố Điện Biên Phủ	094	district.dien_bien_phu	\N	\N	\N	\N	1	2025-05-25	\N	70
191	Thị xã Mường Lay	095	district.muong_lay	\N	\N	\N	\N	1	2025-05-25	\N	70
192	Huyện Mường Nhé	096	district.muong_nhe	\N	\N	\N	\N	1	2025-05-25	\N	70
193	Huyện Mường Chà	097	district.muong_cha	\N	\N	\N	\N	1	2025-05-25	\N	70
194	Huyện Tủa Chùa	098	district.tua_chua	\N	\N	\N	\N	1	2025-05-25	\N	70
195	Huyện Tuần Giáo	099	district.tuan_giao	\N	\N	\N	\N	1	2025-05-25	\N	70
196	Huyện Điện Biên	100	district.dien_bien	\N	\N	\N	\N	1	2025-05-25	\N	70
197	Huyện Điện Biên Đông	101	district.dien_bien_dong	\N	\N	\N	\N	1	2025-05-25	\N	70
198	Huyện Mường Ảng	102	district.muong_ang	\N	\N	\N	\N	1	2025-05-25	\N	70
199	Huyện Nậm Pồ	103	district.nam_po	\N	\N	\N	\N	1	2025-05-25	\N	70
200	Thành phố Lai Châu	105	district.lai_chau	\N	\N	\N	\N	1	2025-05-25	\N	71
201	Huyện Tam Đường	106	district.tam_duong	\N	\N	\N	\N	1	2025-05-25	\N	71
202	Huyện Mường Tè	107	district.muong_te	\N	\N	\N	\N	1	2025-05-25	\N	71
203	Huyện Sìn Hồ	108	district.sin_ho	\N	\N	\N	\N	1	2025-05-25	\N	71
204	Huyện Phong Thổ	109	district.phong_tho	\N	\N	\N	\N	1	2025-05-25	\N	71
205	Huyện Than Uyên	110	district.than_uyen	\N	\N	\N	\N	1	2025-05-25	\N	71
206	Huyện Tân Uyên	111	district.tan_uyen	\N	\N	\N	\N	1	2025-05-25	\N	71
207	Huyện Nậm Nhùn	112	district.nam_nhun	\N	\N	\N	\N	1	2025-05-25	\N	71
208	Thành phố Sơn La	116	district.son_la	\N	\N	\N	\N	1	2025-05-25	\N	72
209	Huyện Quỳnh Nhai	118	district.quynh_nhai	\N	\N	\N	\N	1	2025-05-25	\N	72
210	Huyện Thuận Châu	119	district.thuan_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
211	Huyện Mường La	120	district.muong_la	\N	\N	\N	\N	1	2025-05-25	\N	72
212	Huyện Bắc Yên	121	district.bac_yen	\N	\N	\N	\N	1	2025-05-25	\N	72
213	Huyện Phù Yên	122	district.phu_yen	\N	\N	\N	\N	1	2025-05-25	\N	72
214	Huyện Mộc Châu	123	district.moc_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
215	Huyện Yên Châu	124	district.yen_chau	\N	\N	\N	\N	1	2025-05-25	\N	72
216	Huyện Mai Sơn	125	district.mai_son	\N	\N	\N	\N	1	2025-05-25	\N	72
217	Huyện Sông Mã	126	district.song_ma	\N	\N	\N	\N	1	2025-05-25	\N	72
218	Huyện Sốp Cộp	127	district.sop_cop	\N	\N	\N	\N	1	2025-05-25	\N	72
219	Huyện Vân Hồ	128	district.van_ho	\N	\N	\N	\N	1	2025-05-25	\N	72
220	Thành phố Yên Bái	132	district.yen_bai	\N	\N	\N	\N	1	2025-05-25	\N	73
221	Thị xã Nghĩa Lộ	133	district.nghia_lo	\N	\N	\N	\N	1	2025-05-25	\N	73
222	Huyện Lục Yên	135	district.luc_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
223	Huyện Văn Yên	136	district.van_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
224	Huyện Mù Cang Chải	137	district.mu_cang_chai	\N	\N	\N	\N	1	2025-05-25	\N	73
225	Huyện Trấn Yên	138	district.tran_yen	\N	\N	\N	\N	1	2025-05-25	\N	73
226	Huyện Trạm Tấu	139	district.tram_tau	\N	\N	\N	\N	1	2025-05-25	\N	73
227	Huyện Văn Chấn	140	district.van_chan	\N	\N	\N	\N	1	2025-05-25	\N	73
228	Huyện Yên Bình	141	district.yen_binh	\N	\N	\N	\N	1	2025-05-25	\N	73
229	Thành phố Hạ Long	193	district.ha_long	\N	\N	\N	\N	1	2025-05-25	\N	77
230	Thành phố Móng Cái	194	district.mong_cai	\N	\N	\N	\N	1	2025-05-25	\N	77
231	Thành phố Cẩm Phả	195	district.cam_pha	\N	\N	\N	\N	1	2025-05-25	\N	77
232	Thành phố Uông Bí	196	district.uong_bi	\N	\N	\N	\N	1	2025-05-25	\N	77
233	Huyện Bình Liêu	198	district.binh_lieu	\N	\N	\N	\N	1	2025-05-25	\N	77
234	Huyện Tiên Yên	199	district.tien_yen	\N	\N	\N	\N	1	2025-05-25	\N	77
235	Huyện Đầm Hà	200	district.dam_ha	\N	\N	\N	\N	1	2025-05-25	\N	77
236	Huyện Hải Hà	201	district.hai_ha	\N	\N	\N	\N	1	2025-05-25	\N	77
237	Huyện Ba Chẽ	202	district.ba_che	\N	\N	\N	\N	1	2025-05-25	\N	77
238	Huyện Vân Đồn	203	district.van_don	\N	\N	\N	\N	1	2025-05-25	\N	77
239	Thị xã Đông Triều	205	district.dong_trieu	\N	\N	\N	\N	1	2025-05-25	\N	77
240	Thị xã Quảng Yên	206	district.quang_yen	\N	\N	\N	\N	1	2025-05-25	\N	77
241	Huyện Cô Tô	207	district.co_to	\N	\N	\N	\N	1	2025-05-25	\N	77
242	Thành phố Bắc Giang	213	district.bac_giang	\N	\N	\N	\N	1	2025-05-25	\N	78
243	Huyện Yên Thế	215	district.yen_the	\N	\N	\N	\N	1	2025-05-25	\N	78
244	Huyện Tân Yên	216	district.tan_yen	\N	\N	\N	\N	1	2025-05-25	\N	78
245	Huyện Lạng Giang	217	district.lang_giang	\N	\N	\N	\N	1	2025-05-25	\N	78
246	Huyện Lục Nam	218	district.luc_nam	\N	\N	\N	\N	1	2025-05-25	\N	78
247	Huyện Lục Ngạn	219	district.luc_ngan	\N	\N	\N	\N	1	2025-05-25	\N	78
248	Huyện Sơn Động	220	district.son_dong	\N	\N	\N	\N	1	2025-05-25	\N	78
249	Huyện Yên Dũng	221	district.yen_dung	\N	\N	\N	\N	1	2025-05-25	\N	78
250	Huyện Việt Yên	222	district.viet_yen	\N	\N	\N	\N	1	2025-05-25	\N	78
251	Huyện Hiệp Hòa	223	district.hiep_hoa	\N	\N	\N	\N	1	2025-05-25	\N	78
252	Thành phố Việt Trì	227	district.viet_tri	\N	\N	\N	\N	1	2025-05-25	\N	79
253	Thị xã Phú Thọ	228	district.phu_tho	\N	\N	\N	\N	1	2025-05-25	\N	79
254	Huyện Đoan Hùng	230	district.doan_hung	\N	\N	\N	\N	1	2025-05-25	\N	79
255	Huyện Hạ Hoà	231	district.ha_hoa	\N	\N	\N	\N	1	2025-05-25	\N	79
256	Huyện Thanh Ba	232	district.thanh_ba	\N	\N	\N	\N	1	2025-05-25	\N	79
257	Huyện Phù Ninh	233	district.phu_ninh	\N	\N	\N	\N	1	2025-05-25	\N	79
258	Huyện Yên Lập	234	district.yen_lap	\N	\N	\N	\N	1	2025-05-25	\N	79
259	Huyện Cẩm Khê	235	district.cam_khe	\N	\N	\N	\N	1	2025-05-25	\N	79
260	Huyện Tam Nông	236	district.tam_nong	\N	\N	\N	\N	1	2025-05-25	\N	79
261	Huyện Lâm Thao	237	district.lam_thao	\N	\N	\N	\N	1	2025-05-25	\N	79
262	Huyện Thanh Sơn	238	district.thanh_son	\N	\N	\N	\N	1	2025-05-25	\N	79
263	Huyện Thanh Thủy	239	district.thanh_thuy	\N	\N	\N	\N	1	2025-05-25	\N	79
264	Huyện Tân Sơn	240	district.tan_son	\N	\N	\N	\N	1	2025-05-25	\N	79
265	Thành phố Vĩnh Yên	243	district.vinh_yen	\N	\N	\N	\N	1	2025-05-25	\N	80
266	Thành phố Phúc Yên	244	district.phuc_yen	\N	\N	\N	\N	1	2025-05-25	\N	80
267	Huyện Lập Thạch	246	district.lap_thach	\N	\N	\N	\N	1	2025-05-25	\N	80
268	Huyện Tam Dương	247	district.tam_duong	\N	\N	\N	\N	1	2025-05-25	\N	80
269	Huyện Tam Đảo	248	district.tam_dao	\N	\N	\N	\N	1	2025-05-25	\N	80
270	Huyện Bình Xuyên	249	district.binh_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	80
271	Huyện Yên Lạc	251	district.yen_lac	\N	\N	\N	\N	1	2025-05-25	\N	80
272	Huyện Vĩnh Tường	252	district.vinh_tuong	\N	\N	\N	\N	1	2025-05-25	\N	80
273	Huyện Sông Lô	253	district.song_lo	\N	\N	\N	\N	1	2025-05-25	\N	80
274	Thành phố Bắc Ninh	256	district.bac_ninh	\N	\N	\N	\N	1	2025-05-25	\N	81
275	Huyện Yên Phong	258	district.yen_phong	\N	\N	\N	\N	1	2025-05-25	\N	81
276	Thị xã Quế Võ	259	district.que_vo	\N	\N	\N	\N	1	2025-05-25	\N	81
277	Huyện Tiên Du	260	district.tien_du	\N	\N	\N	\N	1	2025-05-25	\N	81
278	Thành phố Từ Sơn	261	district.tu_son	\N	\N	\N	\N	1	2025-05-25	\N	81
279	Thị xã Thuận Thành	262	district.thuan_thanh	\N	\N	\N	\N	1	2025-05-25	\N	81
280	Huyện Gia Bình	263	district.gia_binh	\N	\N	\N	\N	1	2025-05-25	\N	81
281	Huyện Lương Tài	264	district.luong_tai	\N	\N	\N	\N	1	2025-05-25	\N	81
282	Thành phố Hải Dương	288	district.hai_duong	\N	\N	\N	\N	1	2025-05-25	\N	82
283	Thành phố Chí Linh	290	district.chi_linh	\N	\N	\N	\N	1	2025-05-25	\N	82
284	Huyện Nam Sách	291	district.nam_sach	\N	\N	\N	\N	1	2025-05-25	\N	82
285	Thị xã Kinh Môn	292	district.kinh_mon	\N	\N	\N	\N	1	2025-05-25	\N	82
286	Huyện Kim Thành	293	district.kim_thanh	\N	\N	\N	\N	1	2025-05-25	\N	82
287	Huyện Thanh Hà	294	district.thanh_ha	\N	\N	\N	\N	1	2025-05-25	\N	82
288	Huyện Cẩm Giàng	295	district.cam_giang	\N	\N	\N	\N	1	2025-05-25	\N	82
289	Huyện Bình Giang	296	district.binh_giang	\N	\N	\N	\N	1	2025-05-25	\N	82
290	Huyện Gia Lộc	297	district.gia_loc	\N	\N	\N	\N	1	2025-05-25	\N	82
291	Huyện Tứ Kỳ	298	district.tu_ky	\N	\N	\N	\N	1	2025-05-25	\N	82
292	Huyện Ninh Giang	299	district.ninh_giang	\N	\N	\N	\N	1	2025-05-25	\N	82
293	Huyện Thanh Miện	300	district.thanh_mien	\N	\N	\N	\N	1	2025-05-25	\N	82
294	Quận Hồng Bàng	303	district.hong_bang	\N	\N	\N	\N	1	2025-05-25	\N	83
295	Quận Ngô Quyền	304	district.ngo_quyen	\N	\N	\N	\N	1	2025-05-25	\N	83
296	Quận Lê Chân	305	district.le_chan	\N	\N	\N	\N	1	2025-05-25	\N	83
297	Quận Hải An	306	district.hai_an	\N	\N	\N	\N	1	2025-05-25	\N	83
298	Quận Kiến An	307	district.kien_an	\N	\N	\N	\N	1	2025-05-25	\N	83
299	Quận Đồ Sơn	308	district.do_son	\N	\N	\N	\N	1	2025-05-25	\N	83
300	Quận Dương Kinh	309	district.duong_kinh	\N	\N	\N	\N	1	2025-05-25	\N	83
301	Huyện Thuỷ Nguyên	311	district.thuy_nguyen	\N	\N	\N	\N	1	2025-05-25	\N	83
302	Huyện An Dương	312	district.an_duong	\N	\N	\N	\N	1	2025-05-25	\N	83
303	Huyện An Lão	313	district.an_lao	\N	\N	\N	\N	1	2025-05-25	\N	83
304	Huyện Kiến Thuỵ	314	district.kien_thuy	\N	\N	\N	\N	1	2025-05-25	\N	83
305	Huyện Tiên Lãng	315	district.tien_lang	\N	\N	\N	\N	1	2025-05-25	\N	83
306	Huyện Vĩnh Bảo	316	district.vinh_bao	\N	\N	\N	\N	1	2025-05-25	\N	83
307	Huyện Cát Hải	317	district.cat_hai	\N	\N	\N	\N	1	2025-05-25	\N	83
308	Huyện Bạch Long Vĩ	318	district.bach_long_vi	\N	\N	\N	\N	1	2025-05-25	\N	83
309	Thành phố Hưng Yên	323	district.hung_yen	\N	\N	\N	\N	1	2025-05-25	\N	84
310	Huyện Văn Lâm	325	district.van_lam	\N	\N	\N	\N	1	2025-05-25	\N	84
311	Huyện Văn Giang	326	district.van_giang	\N	\N	\N	\N	1	2025-05-25	\N	84
312	Huyện Yên Mỹ	327	district.yen_my	\N	\N	\N	\N	1	2025-05-25	\N	84
313	Thị xã Mỹ Hào	328	district.my_hao	\N	\N	\N	\N	1	2025-05-25	\N	84
314	Huyện Ân Thi	329	district.an_thi	\N	\N	\N	\N	1	2025-05-25	\N	84
315	Huyện Khoái Châu	330	district.khoai_chau	\N	\N	\N	\N	1	2025-05-25	\N	84
316	Huyện Kim Động	331	district.kim_dong	\N	\N	\N	\N	1	2025-05-25	\N	84
317	Huyện Tiên Lữ	332	district.tien_lu	\N	\N	\N	\N	1	2025-05-25	\N	84
318	Huyện Phù Cừ	333	district.phu_cu	\N	\N	\N	\N	1	2025-05-25	\N	84
319	Thành phố Thái Bình	336	district.thai_binh	\N	\N	\N	\N	1	2025-05-25	\N	85
320	Huyện Quỳnh Phụ	338	district.quynh_phu	\N	\N	\N	\N	1	2025-05-25	\N	85
321	Huyện Hưng Hà	339	district.hung_ha	\N	\N	\N	\N	1	2025-05-25	\N	85
322	Huyện Đông Hưng	340	district.dong_hung	\N	\N	\N	\N	1	2025-05-25	\N	85
323	Huyện Thái Thụy	341	district.thai_thuy	\N	\N	\N	\N	1	2025-05-25	\N	85
324	Huyện Tiền Hải	342	district.tien_hai	\N	\N	\N	\N	1	2025-05-25	\N	85
325	Huyện Kiến Xương	343	district.kien_xuong	\N	\N	\N	\N	1	2025-05-25	\N	85
326	Huyện Vũ Thư	344	district.vu_thu	\N	\N	\N	\N	1	2025-05-25	\N	85
327	Thành phố Phủ Lý	347	district.phu_ly	\N	\N	\N	\N	1	2025-05-25	\N	86
328	Thị xã Duy Tiên	349	district.duy_tien	\N	\N	\N	\N	1	2025-05-25	\N	86
329	Huyện Kim Bảng	350	district.kim_bang	\N	\N	\N	\N	1	2025-05-25	\N	86
330	Huyện Thanh Liêm	351	district.thanh_liem	\N	\N	\N	\N	1	2025-05-25	\N	86
331	Huyện Bình Lục	352	district.binh_luc	\N	\N	\N	\N	1	2025-05-25	\N	86
332	Huyện Lý Nhân	353	district.ly_nhan	\N	\N	\N	\N	1	2025-05-25	\N	86
333	Thành phố Nam Định	356	district.nam_dinh	\N	\N	\N	\N	1	2025-05-25	\N	87
334	Huyện Mỹ Lộc	358	district.my_loc	\N	\N	\N	\N	1	2025-05-25	\N	87
335	Huyện Vụ Bản	359	district.vu_ban	\N	\N	\N	\N	1	2025-05-25	\N	87
336	Huyện Ý Yên	360	district.y_yen	\N	\N	\N	\N	1	2025-05-25	\N	87
337	Huyện Nghĩa Hưng	361	district.nghia_hung	\N	\N	\N	\N	1	2025-05-25	\N	87
338	Huyện Nam Trực	362	district.nam_truc	\N	\N	\N	\N	1	2025-05-25	\N	87
339	Huyện Trực Ninh	363	district.truc_ninh	\N	\N	\N	\N	1	2025-05-25	\N	87
340	Huyện Xuân Trường	364	district.xuan_truong	\N	\N	\N	\N	1	2025-05-25	\N	87
341	Huyện Giao Thủy	365	district.giao_thuy	\N	\N	\N	\N	1	2025-05-25	\N	87
342	Huyện Hải Hậu	366	district.hai_hau	\N	\N	\N	\N	1	2025-05-25	\N	87
343	Thành phố Ninh Bình	369	district.ninh_binh	\N	\N	\N	\N	1	2025-05-25	\N	88
344	Thành phố Tam Điệp	370	district.tam_diep	\N	\N	\N	\N	1	2025-05-25	\N	88
345	Huyện Nho Quan	372	district.nho_quan	\N	\N	\N	\N	1	2025-05-25	\N	88
346	Huyện Gia Viễn	373	district.gia_vien	\N	\N	\N	\N	1	2025-05-25	\N	88
347	Huyện Hoa Lư	374	district.hoa_lu	\N	\N	\N	\N	1	2025-05-25	\N	88
348	Huyện Yên Khánh	375	district.yen_khanh	\N	\N	\N	\N	1	2025-05-25	\N	88
349	Huyện Kim Sơn	376	district.kim_son	\N	\N	\N	\N	1	2025-05-25	\N	88
350	Huyện Yên Mô	377	district.yen_mo	\N	\N	\N	\N	1	2025-05-25	\N	88
351	Thành phố Thanh Hóa	380	district.thanh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	89
352	Thị xã Bỉm Sơn	381	district.bim_son	\N	\N	\N	\N	1	2025-05-25	\N	89
353	Thành phố Sầm Sơn	382	district.sam_son	\N	\N	\N	\N	1	2025-05-25	\N	89
354	Huyện Mường Lát	384	district.muong_lat	\N	\N	\N	\N	1	2025-05-25	\N	89
355	Huyện Quan Hóa	385	district.quan_hoa	\N	\N	\N	\N	1	2025-05-25	\N	89
356	Huyện Bá Thước	386	district.ba_thuoc	\N	\N	\N	\N	1	2025-05-25	\N	89
357	Huyện Quan Sơn	387	district.quan_son	\N	\N	\N	\N	1	2025-05-25	\N	89
358	Huyện Lang Chánh	388	district.lang_chanh	\N	\N	\N	\N	1	2025-05-25	\N	89
359	Huyện Ngọc Lặc	389	district.ngoc_lac	\N	\N	\N	\N	1	2025-05-25	\N	89
360	Huyện Cẩm Thủy	390	district.cam_thuy	\N	\N	\N	\N	1	2025-05-25	\N	89
361	Huyện Thạch Thành	391	district.thach_thanh	\N	\N	\N	\N	1	2025-05-25	\N	89
362	Huyện Hà Trung	392	district.ha_trung	\N	\N	\N	\N	1	2025-05-25	\N	89
363	Huyện Vĩnh Lộc	393	district.vinh_loc	\N	\N	\N	\N	1	2025-05-25	\N	89
364	Huyện Nga Sơn	394	district.nga_son	\N	\N	\N	\N	1	2025-05-25	\N	89
365	Huyện Hậu Lộc	395	district.hau_loc	\N	\N	\N	\N	1	2025-05-25	\N	89
366	Huyện Hoằng Hóa	396	district.hoang_hoa	\N	\N	\N	\N	1	2025-05-25	\N	89
367	Huyện Đông Sơn	397	district.dong_son	\N	\N	\N	\N	1	2025-05-25	\N	89
368	Huyện Quảng Xương	398	district.quang_xuong	\N	\N	\N	\N	1	2025-05-25	\N	89
369	Huyện Nông Cống	399	district.nong_cong	\N	\N	\N	\N	1	2025-05-25	\N	89
370	Huyện Tĩnh Gia	400	district.tinh_gia	\N	\N	\N	\N	1	2025-05-25	\N	89
371	Huyện Triệu Sơn	401	district.trieu_son	\N	\N	\N	\N	1	2025-05-25	\N	89
372	Huyện Thọ Xuân	402	district.tho_xuan	\N	\N	\N	\N	1	2025-05-25	\N	89
373	Huyện Thường Xuân	403	district.thuong_xuan	\N	\N	\N	\N	1	2025-05-25	\N	89
374	Huyện Yên Định	404	district.yen_dinh	\N	\N	\N	\N	1	2025-05-25	\N	89
375	Thị xã Nghi Sơn	405	district.nghi_son	\N	\N	\N	\N	1	2025-05-25	\N	89
376	Huyện Thiệu Hóa	406	district.thieu_hoa	\N	\N	\N	\N	1	2025-05-25	\N	89
377	Huyện Như Thanh	407	district.nhu_thanh	\N	\N	\N	\N	1	2025-05-25	\N	89
378	Huyện Như Xuân	408	district.nhu_xuan	\N	\N	\N	\N	1	2025-05-25	\N	89
379	Thành phố Vinh	412	district.vinh	\N	\N	\N	\N	1	2025-05-25	\N	90
380	Thị xã Cửa Lò	413	district.cua_lo	\N	\N	\N	\N	1	2025-05-25	\N	90
381	Thị xã Thái Hoà	414	district.thai_hoa	\N	\N	\N	\N	1	2025-05-25	\N	90
382	Huyện Quế Phong	415	district.que_phong	\N	\N	\N	\N	1	2025-05-25	\N	90
383	Huyện Tương Dương	416	district.tuong_duong	\N	\N	\N	\N	1	2025-05-25	\N	90
384	Huyện Kỳ Sơn	417	district.ky_son	\N	\N	\N	\N	1	2025-05-25	\N	90
385	Huyện Con Cuông	418	district.con_cuong	\N	\N	\N	\N	1	2025-05-25	\N	90
386	Huyện Anh Sơn	419	district.anh_son	\N	\N	\N	\N	1	2025-05-25	\N	90
387	Huyện Diễn Châu	420	district.dien_chau	\N	\N	\N	\N	1	2025-05-25	\N	90
388	Huyện Yên Thành	421	district.yen_thanh	\N	\N	\N	\N	1	2025-05-25	\N	90
389	Huyện Đô Lương	422	district.do_luong	\N	\N	\N	\N	1	2025-05-25	\N	90
390	Huyện Thanh Chương	423	district.thanh_chuong	\N	\N	\N	\N	1	2025-05-25	\N	90
391	Huyện Nghi Lộc	424	district.nghi_loc	\N	\N	\N	\N	1	2025-05-25	\N	90
392	Huyện Nam Đàn	425	district.nam_dan	\N	\N	\N	\N	1	2025-05-25	\N	90
393	Huyện Hưng Nguyên	426	district.hung_nguyen	\N	\N	\N	\N	1	2025-05-25	\N	90
394	Huyện Quỳ Châu	427	district.quy_chau	\N	\N	\N	\N	1	2025-05-25	\N	90
395	Huyện Quỳ Hợp	428	district.quy_hop	\N	\N	\N	\N	1	2025-05-25	\N	90
396	Huyện Nghĩa Đàn	429	district.nghia_dan	\N	\N	\N	\N	1	2025-05-25	\N	90
397	Huyện Quỳnh Lưu	430	district.quynh_luu	\N	\N	\N	\N	1	2025-05-25	\N	90
398	Thị xã Hoàng Mai	431	district.hoang_mai	\N	\N	\N	\N	1	2025-05-25	\N	90
399	Huyện Tân Kỳ	432	district.tan_ky	\N	\N	\N	\N	1	2025-05-25	\N	90
400	Thành phố Hà Tĩnh	436	district.ha_tinh	\N	\N	\N	\N	1	2025-05-25	\N	91
401	Thị xã Hồng Lĩnh	437	district.hong_linh	\N	\N	\N	\N	1	2025-05-25	\N	91
402	Huyện Hương Sơn	439	district.huong_son	\N	\N	\N	\N	1	2025-05-25	\N	91
403	Huyện Đức Thọ	440	district.duc_tho	\N	\N	\N	\N	1	2025-05-25	\N	91
404	Huyện Vũ Quang	441	district.vu_quang	\N	\N	\N	\N	1	2025-05-25	\N	91
405	Huyện Nghi Xuân	442	district.nghi_xuan	\N	\N	\N	\N	1	2025-05-25	\N	91
406	Huyện Can Lộc	443	district.can_loc	\N	\N	\N	\N	1	2025-05-25	\N	91
407	Huyện Hương Khê	444	district.huong_khe	\N	\N	\N	\N	1	2025-05-25	\N	91
408	Huyện Thạch Hà	445	district.thach_ha	\N	\N	\N	\N	1	2025-05-25	\N	91
409	Huyện Cẩm Xuyên	446	district.cam_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	91
410	Huyện Kỳ Anh	447	district.ky_anh	\N	\N	\N	\N	1	2025-05-25	\N	91
411	Huyện Lộc Hà	448	district.loc_ha	\N	\N	\N	\N	1	2025-05-25	\N	91
412	Thị xã Kỳ Anh	449	district.ky_anh_tx	\N	\N	\N	\N	1	2025-05-25	\N	91
413	Thành phố Đồng Hới	450	district.dong_hoi	\N	\N	\N	\N	1	2025-05-25	\N	92
414	Huyện Minh Hóa	452	district.minh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	92
415	Huyện Tuyên Hóa	453	district.tuyen_hoa	\N	\N	\N	\N	1	2025-05-25	\N	92
499	Thành phố Nha Trang	568	district.nha_trang	\N	\N	\N	\N	1	2025-05-25	\N	100
416	Huyện Quảng Trạch	454	district.quang_trach	\N	\N	\N	\N	1	2025-05-25	\N	92
417	Huyện Bố Trạch	455	district.bo_trach	\N	\N	\N	\N	1	2025-05-25	\N	92
418	Huyện Quảng Ninh	456	district.quang_ninh	\N	\N	\N	\N	1	2025-05-25	\N	92
419	Huyện Lệ Thủy	457	district.le_thuy	\N	\N	\N	\N	1	2025-05-25	\N	92
420	Thị xã Ba Đồn	458	district.ba_don	\N	\N	\N	\N	1	2025-05-25	\N	92
421	Thành phố Đông Hà	461	district.dong_ha	\N	\N	\N	\N	1	2025-05-25	\N	93
422	Thị xã Quảng Trị	462	district.quang_tri_tx	\N	\N	\N	\N	1	2025-05-25	\N	93
423	Huyện Vĩnh Linh	464	district.vinh_linh	\N	\N	\N	\N	1	2025-05-25	\N	93
424	Huyện Hướng Hóa	465	district.huong_hoa	\N	\N	\N	\N	1	2025-05-25	\N	93
425	Huyện Gio Linh	466	district.gio_linh	\N	\N	\N	\N	1	2025-05-25	\N	93
426	Huyện Đa Krông	467	district.da_krong	\N	\N	\N	\N	1	2025-05-25	\N	93
427	Huyện Cam Lộ	468	district.cam_lo	\N	\N	\N	\N	1	2025-05-25	\N	93
428	Huyện Triệu Phong	469	district.trieu_phong	\N	\N	\N	\N	1	2025-05-25	\N	93
429	Huyện Hải Lăng	470	district.hai_lang	\N	\N	\N	\N	1	2025-05-25	\N	93
430	Huyện Cồn Cỏ	471	district.con_co	\N	\N	\N	\N	1	2025-05-25	\N	93
431	Thành phố Huế	474	district.hue	\N	\N	\N	\N	1	2025-05-25	\N	94
432	Huyện Phong Điền	476	district.phong_dien	\N	\N	\N	\N	1	2025-05-25	\N	94
433	Huyện Quảng Điền	477	district.quang_dien	\N	\N	\N	\N	1	2025-05-25	\N	94
434	Huyện Phú Vang	478	district.phu_vang	\N	\N	\N	\N	1	2025-05-25	\N	94
435	Thị xã Hương Thủy	479	district.huong_thuy	\N	\N	\N	\N	1	2025-05-25	\N	94
436	Thị xã Hương Trà	480	district.huong_tra	\N	\N	\N	\N	1	2025-05-25	\N	94
437	Huyện A Lưới	481	district.a_luoi	\N	\N	\N	\N	1	2025-05-25	\N	94
438	Huyện Phú Lộc	482	district.phu_loc	\N	\N	\N	\N	1	2025-05-25	\N	94
439	Huyện Nam Đông	483	district.nam_dong	\N	\N	\N	\N	1	2025-05-25	\N	94
440	Quận Liên Chiểu	490	district.lien_chieu	\N	\N	\N	\N	1	2025-05-25	\N	95
441	Quận Thanh Khê	491	district.thanh_khe	\N	\N	\N	\N	1	2025-05-25	\N	95
442	Quận Hải Châu	492	district.hai_chau	\N	\N	\N	\N	1	2025-05-25	\N	95
443	Quận Sơn Trà	493	district.son_tra	\N	\N	\N	\N	1	2025-05-25	\N	95
444	Quận Ngũ Hành Sơn	494	district.ngu_hanh_son	\N	\N	\N	\N	1	2025-05-25	\N	95
445	Quận Cẩm Lệ	495	district.cam_le	\N	\N	\N	\N	1	2025-05-25	\N	95
446	Huyện Hòa Vang	497	district.hoa_vang	\N	\N	\N	\N	1	2025-05-25	\N	95
447	Huyện Hoàng Sa	498	district.hoang_sa	\N	\N	\N	\N	1	2025-05-25	\N	95
448	Thành phố Tam Kỳ	502	district.tam_ky	\N	\N	\N	\N	1	2025-05-25	\N	96
449	Thành phố Hội An	503	district.hoi_an	\N	\N	\N	\N	1	2025-05-25	\N	96
450	Huyện Tây Giang	504	district.tay_giang	\N	\N	\N	\N	1	2025-05-25	\N	96
451	Huyện Đông Giang	505	district.dong_giang	\N	\N	\N	\N	1	2025-05-25	\N	96
452	Huyện Đại Lộc	506	district.dai_loc	\N	\N	\N	\N	1	2025-05-25	\N	96
453	Thị xã Điện Bàn	507	district.dien_ban	\N	\N	\N	\N	1	2025-05-25	\N	96
454	Huyện Duy Xuyên	508	district.duy_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	96
455	Huyện Quế Sơn	509	district.que_son	\N	\N	\N	\N	1	2025-05-25	\N	96
456	Huyện Nam Giang	510	district.nam_giang	\N	\N	\N	\N	1	2025-05-25	\N	96
457	Huyện Phước Sơn	511	district.phuoc_son	\N	\N	\N	\N	1	2025-05-25	\N	96
458	Huyện Hiệp Đức	512	district.hiep_duc	\N	\N	\N	\N	1	2025-05-25	\N	96
459	Huyện Thăng Bình	513	district.thang_binh	\N	\N	\N	\N	1	2025-05-25	\N	96
460	Huyện Tiên Phước	514	district.tien_phuoc	\N	\N	\N	\N	1	2025-05-25	\N	96
461	Huyện Bắc Trà My	515	district.bac_tra_my	\N	\N	\N	\N	1	2025-05-25	\N	96
462	Huyện Nam Trà My	516	district.nam_tra_my	\N	\N	\N	\N	1	2025-05-25	\N	96
463	Huyện Núi Thành	517	district.nui_thanh	\N	\N	\N	\N	1	2025-05-25	\N	96
464	Huyện Phú Ninh	518	district.phu_ninh	\N	\N	\N	\N	1	2025-05-25	\N	96
465	Huyện Nông Sơn	519	district.nong_son	\N	\N	\N	\N	1	2025-05-25	\N	96
466	Thành phố Quảng Ngãi	522	district.quang_ngai	\N	\N	\N	\N	1	2025-05-25	\N	97
467	Huyện Bình Sơn	524	district.binh_son	\N	\N	\N	\N	1	2025-05-25	\N	97
468	Huyện Trà Bồng	525	district.tra_bong	\N	\N	\N	\N	1	2025-05-25	\N	97
469	Huyện Sơn Tịnh	527	district.son_tinh	\N	\N	\N	\N	1	2025-05-25	\N	97
470	Huyện Tư Nghĩa	528	district.tu_nghia	\N	\N	\N	\N	1	2025-05-25	\N	97
471	Huyện Sơn Hà	529	district.son_ha	\N	\N	\N	\N	1	2025-05-25	\N	97
472	Huyện Sơn Tây	530	district.son_tay	\N	\N	\N	\N	1	2025-05-25	\N	97
473	Huyện Minh Long	531	district.minh_long	\N	\N	\N	\N	1	2025-05-25	\N	97
474	Huyện Nghĩa Hành	532	district.nghia_hanh	\N	\N	\N	\N	1	2025-05-25	\N	97
475	Huyện Mộ Đức	533	district.mo_duc	\N	\N	\N	\N	1	2025-05-25	\N	97
476	Thị xã Đức Phổ	534	district.duc_pho	\N	\N	\N	\N	1	2025-05-25	\N	97
477	Huyện Ba Tơ	535	district.ba_to	\N	\N	\N	\N	1	2025-05-25	\N	97
478	Huyện Lý Sơn	536	district.ly_son	\N	\N	\N	\N	1	2025-05-25	\N	97
479	Thành phố Quy Nhơn	540	district.quy_nhon	\N	\N	\N	\N	1	2025-05-25	\N	98
480	Huyện An Lão	542	district.an_lao	\N	\N	\N	\N	1	2025-05-25	\N	98
481	Thị xã Hoài Nhơn	543	district.hoai_nhon	\N	\N	\N	\N	1	2025-05-25	\N	98
482	Huyện Hoài Ân	544	district.hoai_an	\N	\N	\N	\N	1	2025-05-25	\N	98
483	Huyện Phù Mỹ	545	district.phu_my	\N	\N	\N	\N	1	2025-05-25	\N	98
484	Huyện Vĩnh Thạnh	546	district.vinh_thanh	\N	\N	\N	\N	1	2025-05-25	\N	98
485	Huyện Tây Sơn	547	district.tay_son	\N	\N	\N	\N	1	2025-05-25	\N	98
486	Huyện Phù Cát	548	district.phu_cat	\N	\N	\N	\N	1	2025-05-25	\N	98
487	Thị xã An Nhơn	549	district.an_nhon	\N	\N	\N	\N	1	2025-05-25	\N	98
488	Huyện Tuy Phước	550	district.tuy_phuoc	\N	\N	\N	\N	1	2025-05-25	\N	98
489	Huyện Vân Canh	551	district.van_canh	\N	\N	\N	\N	1	2025-05-25	\N	98
490	Thành phố Tuy Hoà	555	district.tuy_hoa	\N	\N	\N	\N	1	2025-05-25	\N	99
491	Thị xã Sông Cầu	557	district.song_cau	\N	\N	\N	\N	1	2025-05-25	\N	99
492	Huyện Đồng Xuân	558	district.dong_xuan	\N	\N	\N	\N	1	2025-05-25	\N	99
493	Huyện Tuy An	559	district.tuy_an	\N	\N	\N	\N	1	2025-05-25	\N	99
494	Huyện Sơn Hòa	560	district.son_hoa	\N	\N	\N	\N	1	2025-05-25	\N	99
495	Huyện Sông Hinh	561	district.song_hinh	\N	\N	\N	\N	1	2025-05-25	\N	99
496	Huyện Tây Hoà	562	district.tay_hoa	\N	\N	\N	\N	1	2025-05-25	\N	99
497	Huyện Phú Hoà	563	district.phu_hoa	\N	\N	\N	\N	1	2025-05-25	\N	99
498	Thị xã Đông Hòa	564	district.dong_hoa	\N	\N	\N	\N	1	2025-05-25	\N	99
500	Thành phố Cam Ranh	569	district.cam_ranh	\N	\N	\N	\N	1	2025-05-25	\N	100
501	Huyện Cam Lâm	570	district.cam_lam	\N	\N	\N	\N	1	2025-05-25	\N	100
502	Huyện Vạn Ninh	571	district.van_ninh	\N	\N	\N	\N	1	2025-05-25	\N	100
503	Thị xã Ninh Hòa	572	district.ninh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	100
504	Huyện Khánh Vĩnh	573	district.khanh_vinh	\N	\N	\N	\N	1	2025-05-25	\N	100
505	Huyện Diên Khánh	574	district.dien_khanh	\N	\N	\N	\N	1	2025-05-25	\N	100
506	Huyện Khánh Sơn	575	district.khanh_son	\N	\N	\N	\N	1	2025-05-25	\N	100
507	Huyện Trường Sa	576	district.truong_sa	\N	\N	\N	\N	1	2025-05-25	\N	100
508	Thành phố Phan Rang-Tháp Chàm	582	district.phan_rang_thap_cham	\N	\N	\N	\N	1	2025-05-25	\N	101
509	Huyện Bác Ái	584	district.bac_ai	\N	\N	\N	\N	1	2025-05-25	\N	101
510	Huyện Ninh Sơn	585	district.ninh_son	\N	\N	\N	\N	1	2025-05-25	\N	101
511	Huyện Ninh Hải	586	district.ninh_hai	\N	\N	\N	\N	1	2025-05-25	\N	101
512	Huyện Ninh Phước	587	district.ninh_phuoc	\N	\N	\N	\N	1	2025-05-25	\N	101
513	Huyện Thuận Bắc	588	district.thuan_bac	\N	\N	\N	\N	1	2025-05-25	\N	101
514	Huyện Thuận Nam	589	district.thuan_nam	\N	\N	\N	\N	1	2025-05-25	\N	101
515	Thành phố Phan Thiết	593	district.phan_thiet	\N	\N	\N	\N	1	2025-05-25	\N	102
516	Thị xã La Gi	594	district.la_gi	\N	\N	\N	\N	1	2025-05-25	\N	102
517	Huyện Tuy Phong	595	district.tuy_phong	\N	\N	\N	\N	1	2025-05-25	\N	102
518	Huyện Bắc Bình	596	district.bac_binh	\N	\N	\N	\N	1	2025-05-25	\N	102
519	Huyện Hàm Thuận Bắc	597	district.ham_thuan_bac	\N	\N	\N	\N	1	2025-05-25	\N	102
520	Huyện Hàm Thuận Nam	598	district.ham_thuan_nam	\N	\N	\N	\N	1	2025-05-25	\N	102
521	Huyện Tánh Linh	599	district.tanh_linh	\N	\N	\N	\N	1	2025-05-25	\N	102
522	Huyện Đức Linh	600	district.duc_linh	\N	\N	\N	\N	1	2025-05-25	\N	102
523	Huyện Hàm Tân	601	district.ham_tan	\N	\N	\N	\N	1	2025-05-25	\N	102
524	Huyện Phú Quí	602	district.phu_qui	\N	\N	\N	\N	1	2025-05-25	\N	102
525	Thành phố Kon Tum	608	district.kon_tum	\N	\N	\N	\N	1	2025-05-25	\N	103
526	Huyện Đắk Glei	610	district.dak_glei	\N	\N	\N	\N	1	2025-05-25	\N	103
527	Huyện Ngọc Hồi	611	district.ngoc_hoi	\N	\N	\N	\N	1	2025-05-25	\N	103
528	Huyện Đắk Tô	612	district.dak_to	\N	\N	\N	\N	1	2025-05-25	\N	103
529	Huyện Kon Plông	613	district.kon_plong	\N	\N	\N	\N	1	2025-05-25	\N	103
530	Huyện Kon Rẫy	614	district.kon_ray	\N	\N	\N	\N	1	2025-05-25	\N	103
531	Huyện Đắk Hà	615	district.dak_ha	\N	\N	\N	\N	1	2025-05-25	\N	103
532	Huyện Sa Thầy	616	district.sa_thay	\N	\N	\N	\N	1	2025-05-25	\N	103
533	Huyện Tu Mơ Rông	617	district.tu_mo_rong	\N	\N	\N	\N	1	2025-05-25	\N	103
534	Huyện Ia H' Drai	618	district.ia_h_drai	\N	\N	\N	\N	1	2025-05-25	\N	103
535	Thành phố Pleiku	622	district.pleiku	\N	\N	\N	\N	1	2025-05-25	\N	104
536	Thị xã An Khê	623	district.an_khe	\N	\N	\N	\N	1	2025-05-25	\N	104
537	Thị xã Ayun Pa	624	district.ayun_pa	\N	\N	\N	\N	1	2025-05-25	\N	104
538	Huyện KBang	625	district.kbang	\N	\N	\N	\N	1	2025-05-25	\N	104
539	Huyện Đăk Đoa	626	district.dak_doa	\N	\N	\N	\N	1	2025-05-25	\N	104
540	Huyện Chư Păh	627	district.chu_pah	\N	\N	\N	\N	1	2025-05-25	\N	104
541	Huyện Ia Grai	628	district.ia_grai	\N	\N	\N	\N	1	2025-05-25	\N	104
542	Huyện Mang Yang	629	district.mang_yang	\N	\N	\N	\N	1	2025-05-25	\N	104
543	Huyện Kông Chro	630	district.kong_chro	\N	\N	\N	\N	1	2025-05-25	\N	104
544	Huyện Đức Cơ	631	district.duc_co	\N	\N	\N	\N	1	2025-05-25	\N	104
545	Huyện Chư Prông	632	district.chu_prong	\N	\N	\N	\N	1	2025-05-25	\N	104
546	Huyện Chư Sê	633	district.chu_se	\N	\N	\N	\N	1	2025-05-25	\N	104
547	Huyện Đăk Pơ	634	district.dak_po	\N	\N	\N	\N	1	2025-05-25	\N	104
548	Huyện Ia Pa	635	district.ia_pa	\N	\N	\N	\N	1	2025-05-25	\N	104
549	Huyện Krông Pa	637	district.krong_pa	\N	\N	\N	\N	1	2025-05-25	\N	104
550	Huyện Phú Thiện	638	district.phu_thien	\N	\N	\N	\N	1	2025-05-25	\N	104
551	Huyện Chư Pưh	639	district.chu_puh	\N	\N	\N	\N	1	2025-05-25	\N	104
552	Thành phố Buôn Ma Thuột	643	district.buon_ma_thuot	\N	\N	\N	\N	1	2025-05-25	\N	105
553	Thị xã Buôn Hồ	644	district.buon_ho	\N	\N	\N	\N	1	2025-05-25	\N	105
554	Huyện Ea H'leo	645	district.ea_hleo	\N	\N	\N	\N	1	2025-05-25	\N	105
555	Huyện Ea Súp	646	district.ea_sup	\N	\N	\N	\N	1	2025-05-25	\N	105
556	Huyện Buôn Đôn	647	district.buon_don	\N	\N	\N	\N	1	2025-05-25	\N	105
557	Huyện Cư M'gar	648	district.cu_mgar	\N	\N	\N	\N	1	2025-05-25	\N	105
558	Huyện Krông Búk	649	district.krong_buk	\N	\N	\N	\N	1	2025-05-25	\N	105
559	Huyện Krông Năng	650	district.krong_nang	\N	\N	\N	\N	1	2025-05-25	\N	105
560	Huyện Ea Kar	651	district.ea_kar	\N	\N	\N	\N	1	2025-05-25	\N	105
561	Huyện M'Đrắk	652	district.mdrak	\N	\N	\N	\N	1	2025-05-25	\N	105
562	Huyện Krông Bông	653	district.krong_bong	\N	\N	\N	\N	1	2025-05-25	\N	105
563	Huyện Krông Pắc	654	district.krong_pac	\N	\N	\N	\N	1	2025-05-25	\N	105
564	Huyện Krông A Na	655	district.krong_a_na	\N	\N	\N	\N	1	2025-05-25	\N	105
565	Huyện Lắk	656	district.lak	\N	\N	\N	\N	1	2025-05-25	\N	105
566	Huyện Cư Kuin	657	district.cu_kuin	\N	\N	\N	\N	1	2025-05-25	\N	105
567	Thành phố Gia Nghĩa	660	district.gia_nghia	\N	\N	\N	\N	1	2025-05-25	\N	106
568	Huyện Đăk Glong	661	district.dak_glong	\N	\N	\N	\N	1	2025-05-25	\N	106
569	Huyện Cư Jút	662	district.cu_jut	\N	\N	\N	\N	1	2025-05-25	\N	106
570	Huyện Đắk Mil	663	district.dak_mil	\N	\N	\N	\N	1	2025-05-25	\N	106
571	Huyện Krông Nô	664	district.krong_no	\N	\N	\N	\N	1	2025-05-25	\N	106
572	Huyện Đắk Song	665	district.dak_song	\N	\N	\N	\N	1	2025-05-25	\N	106
573	Huyện Đắk R'Lấp	666	district.dak_rlap	\N	\N	\N	\N	1	2025-05-25	\N	106
574	Huyện Tuy Đức	667	district.tuy_duc	\N	\N	\N	\N	1	2025-05-25	\N	106
575	Thành phố Đà Lạt	672	district.da_lat	\N	\N	\N	\N	1	2025-05-25	\N	107
576	Thành phố Bảo Lộc	673	district.bao_loc	\N	\N	\N	\N	1	2025-05-25	\N	107
577	Huyện Đam Rông	674	district.dam_rong	\N	\N	\N	\N	1	2025-05-25	\N	107
578	Huyện Lạc Dương	675	district.lac_duong	\N	\N	\N	\N	1	2025-05-25	\N	107
579	Huyện Lâm Hà	676	district.lam_ha	\N	\N	\N	\N	1	2025-05-25	\N	107
580	Huyện Đơn Dương	677	district.don_duong	\N	\N	\N	\N	1	2025-05-25	\N	107
581	Huyện Đức Trọng	678	district.duc_trong	\N	\N	\N	\N	1	2025-05-25	\N	107
582	Huyện Di Linh	679	district.di_linh	\N	\N	\N	\N	1	2025-05-25	\N	107
583	Huyện Bảo Lâm	680	district.bao_lam	\N	\N	\N	\N	1	2025-05-25	\N	107
584	Huyện Đạ Huoai	681	district.da_huoai	\N	\N	\N	\N	1	2025-05-25	\N	107
585	Huyện Đạ Tẻh	682	district.da_teh	\N	\N	\N	\N	1	2025-05-25	\N	107
586	Huyện Cát Tiên	683	district.cat_tien	\N	\N	\N	\N	1	2025-05-25	\N	107
587	Thị xã Phước Long	688	district.phuoc_long	\N	\N	\N	\N	1	2025-05-25	\N	108
588	Thành phố Đồng Xoài	689	district.dong_xoai	\N	\N	\N	\N	1	2025-05-25	\N	108
589	Thị xã Bình Long	690	district.binh_long	\N	\N	\N	\N	1	2025-05-25	\N	108
590	Huyện Bù Gia Mập	691	district.bu_gia_map	\N	\N	\N	\N	1	2025-05-25	\N	108
591	Huyện Lộc Ninh	692	district.loc_ninh	\N	\N	\N	\N	1	2025-05-25	\N	108
592	Huyện Bù Đốp	693	district.bu_dop	\N	\N	\N	\N	1	2025-05-25	\N	108
593	Huyện Hớn Quản	694	district.hon_quan	\N	\N	\N	\N	1	2025-05-25	\N	108
594	Huyện Đồng Phú	695	district.dong_phu	\N	\N	\N	\N	1	2025-05-25	\N	108
595	Huyện Bù Đăng	696	district.bu_dang	\N	\N	\N	\N	1	2025-05-25	\N	108
596	Thị xã Chơn Thành	697	district.chon_thanh	\N	\N	\N	\N	1	2025-05-25	\N	108
597	Huyện Phú Riềng	698	district.phu_rieng	\N	\N	\N	\N	1	2025-05-25	\N	108
598	Thành phố Tây Ninh	703	district.tay_ninh	\N	\N	\N	\N	1	2025-05-25	\N	109
599	Huyện Tân Biên	705	district.tan_bien	\N	\N	\N	\N	1	2025-05-25	\N	109
600	Huyện Tân Châu	706	district.tan_chau	\N	\N	\N	\N	1	2025-05-25	\N	109
601	Huyện Dương Minh Châu	707	district.duong_minh_chau	\N	\N	\N	\N	1	2025-05-25	\N	109
602	Huyện Châu Thành	708	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	109
603	Thị xã Hòa Thành	709	district.hoa_thanh	\N	\N	\N	\N	1	2025-05-25	\N	109
604	Huyện Gò Dầu	710	district.go_dau	\N	\N	\N	\N	1	2025-05-25	\N	109
605	Huyện Bến Cầu	711	district.ben_cau	\N	\N	\N	\N	1	2025-05-25	\N	109
606	Thị xã Trảng Bàng	712	district.trang_bang	\N	\N	\N	\N	1	2025-05-25	\N	109
607	Thành phố Thủ Dầu Một	718	district.thu_dau_mot	\N	\N	\N	\N	1	2025-05-25	\N	110
608	Huyện Bàu Bàng	719	district.bau_bang	\N	\N	\N	\N	1	2025-05-25	\N	110
609	Huyện Dầu Tiếng	720	district.dau_tieng	\N	\N	\N	\N	1	2025-05-25	\N	110
610	Thị xã Bến Cát	721	district.ben_cat	\N	\N	\N	\N	1	2025-05-25	\N	110
611	Huyện Phú Giáo	722	district.phu_giao	\N	\N	\N	\N	1	2025-05-25	\N	110
612	Thị xã Tân Uyên	723	district.tan_uyen	\N	\N	\N	\N	1	2025-05-25	\N	110
613	Thành phố Dĩ An	724	district.di_an	\N	\N	\N	\N	1	2025-05-25	\N	110
614	Thành phố Thuận An	725	district.thuan_an	\N	\N	\N	\N	1	2025-05-25	\N	110
615	Huyện Bắc Tân Uyên	726	district.bac_tan_uyen	\N	\N	\N	\N	1	2025-05-25	\N	110
616	Thành phố Biên Hòa	731	district.bien_hoa	\N	\N	\N	\N	1	2025-05-25	\N	111
617	Thành phố Long Khánh	732	district.long_khanh	\N	\N	\N	\N	1	2025-05-25	\N	111
618	Huyện Tân Phú	734	district.tan_phu	\N	\N	\N	\N	1	2025-05-25	\N	111
619	Huyện Vĩnh Cửu	735	district.vinh_cuu	\N	\N	\N	\N	1	2025-05-25	\N	111
620	Huyện Định Quán	736	district.dinh_quan	\N	\N	\N	\N	1	2025-05-25	\N	111
621	Huyện Trảng Bom	737	district.trang_bom	\N	\N	\N	\N	1	2025-05-25	\N	111
622	Huyện Thống Nhất	738	district.thong_nhat	\N	\N	\N	\N	1	2025-05-25	\N	111
623	Huyện Cẩm Mỹ	739	district.cam_my	\N	\N	\N	\N	1	2025-05-25	\N	111
624	Huyện Long Thành	740	district.long_thanh	\N	\N	\N	\N	1	2025-05-25	\N	111
625	Huyện Xuân Lộc	741	district.xuan_loc	\N	\N	\N	\N	1	2025-05-25	\N	111
626	Huyện Nhơn Trạch	742	district.nhon_trach	\N	\N	\N	\N	1	2025-05-25	\N	111
627	Thành phố Vũng Tàu	747	district.vung_tau	\N	\N	\N	\N	1	2025-05-25	\N	112
628	Thành phố Bà Rịa	748	district.ba_ria	\N	\N	\N	\N	1	2025-05-25	\N	112
629	Huyện Châu Đức	750	district.chau_duc	\N	\N	\N	\N	1	2025-05-25	\N	112
630	Huyện Xuyên Mộc	751	district.xuyen_moc	\N	\N	\N	\N	1	2025-05-25	\N	112
631	Huyện Long Điền	752	district.long_dien	\N	\N	\N	\N	1	2025-05-25	\N	112
632	Huyện Đất Đỏ	753	district.dat_do	\N	\N	\N	\N	1	2025-05-25	\N	112
633	Thị xã Phú Mỹ	754	district.phu_my	\N	\N	\N	\N	1	2025-05-25	\N	112
634	Huyện Côn Đảo	755	district.con_dao	\N	\N	\N	\N	1	2025-05-25	\N	112
635	Quận 1	760	district.quan_1	\N	\N	\N	\N	1	2025-05-25	\N	113
636	Quận 12	761	district.quan_12	\N	\N	\N	\N	1	2025-05-25	\N	113
637	Quận Gò Vấp	764	district.go_vap	\N	\N	\N	\N	1	2025-05-25	\N	113
638	Quận Bình Thạnh	765	district.binh_thanh	\N	\N	\N	\N	1	2025-05-25	\N	113
639	Quận Phú Nhuận	766	district.phu_nhuan	\N	\N	\N	\N	1	2025-05-25	\N	113
640	Quận Tân Bình	767	district.tan_binh	\N	\N	\N	\N	1	2025-05-25	\N	113
641	Quận Tân Phú	768	district.tan_phu	\N	\N	\N	\N	1	2025-05-25	\N	113
642	Thành phố Thủ Đức	769	district.thu_duc	\N	\N	\N	\N	1	2025-05-25	\N	113
643	Quận 3	770	district.quan_3	\N	\N	\N	\N	1	2025-05-25	\N	113
644	Quận 10	771	district.quan_10	\N	\N	\N	\N	1	2025-05-25	\N	113
645	Quận 11	772	district.quan_11	\N	\N	\N	\N	1	2025-05-25	\N	113
646	Quận 4	773	district.quan_4	\N	\N	\N	\N	1	2025-05-25	\N	113
647	Quận 5	774	district.quan_5	\N	\N	\N	\N	1	2025-05-25	\N	113
648	Quận 6	775	district.quan_6	\N	\N	\N	\N	1	2025-05-25	\N	113
649	Quận 8	776	district.quan_8	\N	\N	\N	\N	1	2025-05-25	\N	113
650	Quận Bình Tân	777	district.binh_tan	\N	\N	\N	\N	1	2025-05-25	\N	113
651	Quận 7	778	district.quan_7	\N	\N	\N	\N	1	2025-05-25	\N	113
652	Huyện Củ Chi	783	district.cu_chi	\N	\N	\N	\N	1	2025-05-25	\N	113
653	Huyện Hóc Môn	784	district.hoc_mon	\N	\N	\N	\N	1	2025-05-25	\N	113
654	Huyện Bình Chánh	785	district.binh_chanh	\N	\N	\N	\N	1	2025-05-25	\N	113
655	Huyện Nhà Bè	786	district.nha_be	\N	\N	\N	\N	1	2025-05-25	\N	113
656	Huyện Cần Giờ	787	district.can_gio	\N	\N	\N	\N	1	2025-05-25	\N	113
657	Thành phố Tân An	794	district.tan_an	\N	\N	\N	\N	1	2025-05-25	\N	114
658	Thị xã Kiến Tường	795	district.kien_tuong	\N	\N	\N	\N	1	2025-05-25	\N	114
659	Huyện Tân Hưng	796	district.tan_hung	\N	\N	\N	\N	1	2025-05-25	\N	114
660	Huyện Vĩnh Hưng	797	district.vinh_hung	\N	\N	\N	\N	1	2025-05-25	\N	114
661	Huyện Mộc Hóa	798	district.moc_hoa	\N	\N	\N	\N	1	2025-05-25	\N	114
662	Huyện Tân Thạnh	799	district.tan_thanh	\N	\N	\N	\N	1	2025-05-25	\N	114
663	Huyện Thạnh Hóa	800	district.thanh_hoa	\N	\N	\N	\N	1	2025-05-25	\N	114
664	Huyện Đức Huệ	801	district.duc_hue	\N	\N	\N	\N	1	2025-05-25	\N	114
665	Huyện Đức Hòa	802	district.duc_hoa	\N	\N	\N	\N	1	2025-05-25	\N	114
666	Huyện Bến Lức	803	district.ben_luc	\N	\N	\N	\N	1	2025-05-25	\N	114
667	Huyện Thủ Thừa	804	district.thu_thua	\N	\N	\N	\N	1	2025-05-25	\N	114
668	Huyện Tân Trụ	805	district.tan_tru	\N	\N	\N	\N	1	2025-05-25	\N	114
669	Huyện Cần Đước	806	district.can_duoc	\N	\N	\N	\N	1	2025-05-25	\N	114
670	Huyện Cần Giuộc	807	district.can_giuoc	\N	\N	\N	\N	1	2025-05-25	\N	114
671	Huyện Châu Thành	808	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	114
672	Thành phố Mỹ Tho	815	district.my_tho	\N	\N	\N	\N	1	2025-05-25	\N	115
673	Thị xã Gò Công	816	district.go_cong_tx	\N	\N	\N	\N	1	2025-05-25	\N	115
674	Thị xã Cai Lậy	817	district.cai_lay_tx	\N	\N	\N	\N	1	2025-05-25	\N	115
675	Huyện Tân Phước	818	district.tan_phuoc	\N	\N	\N	\N	1	2025-05-25	\N	115
676	Huyện Cái Bè	819	district.cai_be	\N	\N	\N	\N	1	2025-05-25	\N	115
677	Huyện Cai Lậy	820	district.cai_lay	\N	\N	\N	\N	1	2025-05-25	\N	115
678	Huyện Châu Thành	821	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	115
679	Huyện Chợ Gạo	822	district.cho_gao	\N	\N	\N	\N	1	2025-05-25	\N	115
680	Huyện Gò Công Tây	823	district.go_cong_tay	\N	\N	\N	\N	1	2025-05-25	\N	115
681	Huyện Gò Công Đông	824	district.go_cong_dong	\N	\N	\N	\N	1	2025-05-25	\N	115
682	Huyện Tân Phú Đông	825	district.tan_phu_dong	\N	\N	\N	\N	1	2025-05-25	\N	115
683	Thành phố Bến Tre	829	district.ben_tre	\N	\N	\N	\N	1	2025-05-25	\N	116
684	Huyện Châu Thành	831	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	116
685	Huyện Chợ Lách	832	district.cho_lach	\N	\N	\N	\N	1	2025-05-25	\N	116
686	Huyện Mỏ Cày Nam	833	district.mo_cay_nam	\N	\N	\N	\N	1	2025-05-25	\N	116
687	Huyện Giồng Trôm	834	district.giong_trom	\N	\N	\N	\N	1	2025-05-25	\N	116
688	Huyện Bình Đại	835	district.binh_dai	\N	\N	\N	\N	1	2025-05-25	\N	116
689	Huyện Ba Tri	836	district.ba_tri	\N	\N	\N	\N	1	2025-05-25	\N	116
690	Huyện Thạnh Phú	837	district.thanh_phu	\N	\N	\N	\N	1	2025-05-25	\N	116
691	Huyện Mỏ Cày Bắc	838	district.mo_cay_bac	\N	\N	\N	\N	1	2025-05-25	\N	116
692	Thành phố Trà Vinh	842	district.tra_vinh	\N	\N	\N	\N	1	2025-05-25	\N	117
693	Huyện Càng Long	844	district.cang_long	\N	\N	\N	\N	1	2025-05-25	\N	117
694	Huyện Cầu Kè	845	district.cau_ke	\N	\N	\N	\N	1	2025-05-25	\N	117
695	Huyện Tiểu Cần	846	district.tieu_can	\N	\N	\N	\N	1	2025-05-25	\N	117
696	Huyện Châu Thành	847	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	117
697	Huyện Cầu Ngang	848	district.cau_ngang	\N	\N	\N	\N	1	2025-05-25	\N	117
698	Huyện Trà Cú	849	district.tra_cu	\N	\N	\N	\N	1	2025-05-25	\N	117
699	Huyện Duyên Hải	850	district.duyen_hai	\N	\N	\N	\N	1	2025-05-25	\N	117
700	Thị xã Duyên Hải	851	district.duyen_hai_tx	\N	\N	\N	\N	1	2025-05-25	\N	117
701	Thành phố Vĩnh Long	855	district.vinh_long	\N	\N	\N	\N	1	2025-05-25	\N	118
702	Huyện Long Hồ	857	district.long_ho	\N	\N	\N	\N	1	2025-05-25	\N	118
703	Huyện Mang Thít	858	district.mang_thit	\N	\N	\N	\N	1	2025-05-25	\N	118
704	Huyện Vũng Liêm	859	district.vung_liem	\N	\N	\N	\N	1	2025-05-25	\N	118
705	Huyện Tam Bình	860	district.tam_binh	\N	\N	\N	\N	1	2025-05-25	\N	118
706	Thị xã Bình Minh	861	district.binh_minh	\N	\N	\N	\N	1	2025-05-25	\N	118
707	Huyện Trà Ôn	862	district.tra_on	\N	\N	\N	\N	1	2025-05-25	\N	118
708	Huyện Bình Tân	863	district.binh_tan	\N	\N	\N	\N	1	2025-05-25	\N	118
709	Thành phố Cao Lãnh	866	district.cao_lanh_tp	\N	\N	\N	\N	1	2025-05-25	\N	119
710	Thành phố Sa Đéc	867	district.sa_dec	\N	\N	\N	\N	1	2025-05-25	\N	119
711	Thành phố Hồng Ngự	868	district.hong_ngu_tp	\N	\N	\N	\N	1	2025-05-25	\N	119
712	Huyện Tân Hồng	869	district.tan_hong	\N	\N	\N	\N	1	2025-05-25	\N	119
713	Huyện Hồng Ngự	870	district.hong_ngu	\N	\N	\N	\N	1	2025-05-25	\N	119
714	Huyện Tam Nông	871	district.tam_nong	\N	\N	\N	\N	1	2025-05-25	\N	119
715	Huyện Tháp Mười	872	district.thap_muoi	\N	\N	\N	\N	1	2025-05-25	\N	119
716	Huyện Cao Lãnh	873	district.cao_lanh	\N	\N	\N	\N	1	2025-05-25	\N	119
717	Huyện Thanh Bình	874	district.thanh_binh	\N	\N	\N	\N	1	2025-05-25	\N	119
718	Huyện Lấp Vò	875	district.lap_vo	\N	\N	\N	\N	1	2025-05-25	\N	119
719	Huyện Lai Vung	876	district.lai_vung	\N	\N	\N	\N	1	2025-05-25	\N	119
720	Huyện Châu Thành	877	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	119
721	Thành phố Long Xuyên	883	district.long_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	120
722	Thành phố Châu Đốc	884	district.chau_doc	\N	\N	\N	\N	1	2025-05-25	\N	120
723	Huyện An Phú	886	district.an_phu	\N	\N	\N	\N	1	2025-05-25	\N	120
724	Thị xã Tân Châu	887	district.tan_chau_tx	\N	\N	\N	\N	1	2025-05-25	\N	120
725	Huyện Phú Tân	888	district.phu_tan	\N	\N	\N	\N	1	2025-05-25	\N	120
726	Huyện Châu Phú	889	district.chau_phu	\N	\N	\N	\N	1	2025-05-25	\N	120
727	Huyện Tịnh Biên	890	district.tinh_bien	\N	\N	\N	\N	1	2025-05-25	\N	120
728	Huyện Tri Tôn	891	district.tri_ton	\N	\N	\N	\N	1	2025-05-25	\N	120
729	Huyện Châu Thành	892	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	120
730	Huyện Chợ Mới	893	district.cho_moi	\N	\N	\N	\N	1	2025-05-25	\N	120
731	Huyện Thoại Sơn	894	district.thoai_son	\N	\N	\N	\N	1	2025-05-25	\N	120
732	Thành phố Rạch Giá	899	district.rach_gia	\N	\N	\N	\N	1	2025-05-25	\N	121
733	Thành phố Hà Tiên	900	district.ha_tien	\N	\N	\N	\N	1	2025-05-25	\N	121
734	Huyện Kiên Lương	902	district.kien_luong	\N	\N	\N	\N	1	2025-05-25	\N	121
735	Huyện Hòn Đất	903	district.hon_dat	\N	\N	\N	\N	1	2025-05-25	\N	121
736	Huyện Tân Hiệp	904	district.tan_hiep	\N	\N	\N	\N	1	2025-05-25	\N	121
737	Huyện Châu Thành	905	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	121
738	Huyện Giồng Riềng	906	district.giong_rieng	\N	\N	\N	\N	1	2025-05-25	\N	121
739	Huyện Gò Quao	907	district.go_quao	\N	\N	\N	\N	1	2025-05-25	\N	121
740	Huyện An Biên	908	district.an_bien	\N	\N	\N	\N	1	2025-05-25	\N	121
741	Huyện An Minh	909	district.an_minh	\N	\N	\N	\N	1	2025-05-25	\N	121
742	Huyện Vĩnh Thuận	910	district.vinh_thuan	\N	\N	\N	\N	1	2025-05-25	\N	121
743	Thành phố Phú Quốc	911	district.phu_quoc	\N	\N	\N	\N	1	2025-05-25	\N	121
744	Huyện Kiên Hải	912	district.kien_hai	\N	\N	\N	\N	1	2025-05-25	\N	121
745	Huyện U Minh Thượng	913	district.u_minh_thuong	\N	\N	\N	\N	1	2025-05-25	\N	121
746	Huyện Giang Thành	914	district.giang_thanh	\N	\N	\N	\N	1	2025-05-25	\N	121
747	Quận Ninh Kiều	916	district.ninh_kieu	\N	\N	\N	\N	1	2025-05-25	\N	122
748	Quận Ô Môn	917	district.o_mon	\N	\N	\N	\N	1	2025-05-25	\N	122
749	Quận Bình Thuỷ	918	district.binh_thuy	\N	\N	\N	\N	1	2025-05-25	\N	122
750	Quận Cái Răng	919	district.cai_rang	\N	\N	\N	\N	1	2025-05-25	\N	122
751	Quận Thốt Nốt	923	district.thot_not	\N	\N	\N	\N	1	2025-05-25	\N	122
752	Huyện Vĩnh Thạnh	924	district.vinh_thanh	\N	\N	\N	\N	1	2025-05-25	\N	122
753	Huyện Cờ Đỏ	925	district.co_do	\N	\N	\N	\N	1	2025-05-25	\N	122
754	Huyện Phong Điền	926	district.phong_dien	\N	\N	\N	\N	1	2025-05-25	\N	122
755	Huyện Thới Lai	927	district.thoi_lai	\N	\N	\N	\N	1	2025-05-25	\N	122
756	Thành phố Vị Thanh	930	district.vi_thanh	\N	\N	\N	\N	1	2025-05-25	\N	123
757	Thành phố Ngã Bảy	931	district.nga_bay	\N	\N	\N	\N	1	2025-05-25	\N	123
758	Huyện Châu Thành A	932	district.chau_thanh_a	\N	\N	\N	\N	1	2025-05-25	\N	123
759	Huyện Châu Thành	933	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	123
760	Huyện Phụng Hiệp	934	district.phung_hiep	\N	\N	\N	\N	1	2025-05-25	\N	123
761	Huyện Vị Thuỷ	935	district.vi_thuy	\N	\N	\N	\N	1	2025-05-25	\N	123
762	Huyện Long Mỹ	936	district.long_my	\N	\N	\N	\N	1	2025-05-25	\N	123
763	Thị xã Long Mỹ	937	district.long_my_tx	\N	\N	\N	\N	1	2025-05-25	\N	123
764	Thành phố Sóc Trăng	941	district.soc_trang	\N	\N	\N	\N	1	2025-05-25	\N	124
765	Huyện Châu Thành	942	district.chau_thanh	\N	\N	\N	\N	1	2025-05-25	\N	124
766	Huyện Kế Sách	943	district.ke_sach	\N	\N	\N	\N	1	2025-05-25	\N	124
767	Huyện Mỹ Tú	944	district.my_tu	\N	\N	\N	\N	1	2025-05-25	\N	124
768	Huyện Cù Lao Dung	945	district.cu_lao_dung	\N	\N	\N	\N	1	2025-05-25	\N	124
769	Huyện Long Phú	946	district.long_phu	\N	\N	\N	\N	1	2025-05-25	\N	124
770	Huyện Mỹ Xuyên	947	district.my_xuyen	\N	\N	\N	\N	1	2025-05-25	\N	124
771	Thị xã Ngã Năm	948	district.nga_nam	\N	\N	\N	\N	1	2025-05-25	\N	124
772	Huyện Thạnh Trị	949	district.thanh_tri	\N	\N	\N	\N	1	2025-05-25	\N	124
773	Thị xã Vĩnh Châu	950	district.vinh_chau	\N	\N	\N	\N	1	2025-05-25	\N	124
774	Huyện Trần Đề	951	district.tran_de	\N	\N	\N	\N	1	2025-05-25	\N	124
775	Thành phố Bạc Liêu	954	district.bac_lieu	\N	\N	\N	\N	1	2025-05-25	\N	125
776	Huyện Hồng Dân	956	district.hong_dan	\N	\N	\N	\N	1	2025-05-25	\N	125
777	Huyện Phước Long	957	district.phuoc_long	\N	\N	\N	\N	1	2025-05-25	\N	125
778	Huyện Vĩnh Lợi	958	district.vinh_loi	\N	\N	\N	\N	1	2025-05-25	\N	125
779	Thị xã Giá Rai	959	district.gia_rai	\N	\N	\N	\N	1	2025-05-25	\N	125
780	Huyện Đông Hải	960	district.dong_hai	\N	\N	\N	\N	1	2025-05-25	\N	125
781	Huyện Hoà Bình	961	district.hoa_binh	\N	\N	\N	\N	1	2025-05-25	\N	125
782	Thành phố Cà Mau	964	district.ca_mau	\N	\N	\N	\N	1	2025-05-25	\N	126
783	Huyện U Minh	966	district.u_minh	\N	\N	\N	\N	1	2025-05-25	\N	126
784	Huyện Thới Bình	967	district.thoi_binh	\N	\N	\N	\N	1	2025-05-25	\N	126
785	Huyện Trần Văn Thời	968	district.tran_van_thoi	\N	\N	\N	\N	1	2025-05-25	\N	126
786	Huyện Cái Nước	969	district.cai_nuoc	\N	\N	\N	\N	1	2025-05-25	\N	126
787	Huyện Đầm Dơi	970	district.dam_doi	\N	\N	\N	\N	1	2025-05-25	\N	126
788	Huyện Năm Căn	971	district.nam_can	\N	\N	\N	\N	1	2025-05-25	\N	126
789	Huyện Phú Tân	972	district.phu_tan	\N	\N	\N	\N	1	2025-05-25	\N	126
790	Huyện Ngọc Hiển	973	district.ngoc_hien	\N	\N	\N	\N	1	2025-05-25	\N	126
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name, description, is_default, created_at, updated_at) FROM stdin;
1	user	\N	t	2025-05-22 22:12:32	\N
2	Editor	Can edit content	f	2025-05-22 16:01:39.275657	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, full_name, hashed_password, role_id, is_active, is_superuser, created_at, updated_at) FROM stdin;
1	user@example.com	admin	$2b$12$gWr2/uZxyfN94UlbfA5wVOFWS7e8gWuSMx63bye5dZOhPA/6OFBnu	1	t	t	2025-05-22 15:54:38.309696	2025-05-24 01:31:08.393934
\.


--
-- Data for Name: wards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wards (id, name, code, name_code, description, description_code, background_image, logo, status, created_date, updated_date, district_id) FROM stdin;
\.


--
-- Data for Name: accommodations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accommodations (id, user_id, name, name_code, description, description_code, latitude, longitude, geom, address, city, country_id, region_id, district_id, ward_id, category_id, thumbnail_url, price_min, price_max, popularity_score, checkin_time, checkout_time, cancel_policy, pet_policy, child_policy, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: accommodation_rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accommodation_rooms (id, accommodation_id, name, name_code, description, description_code, adult_capacity, child_capacity, room_area, bed_capacity, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
initial_migration
\.


--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article (id, author_id, title, title_code, description, description_code, content, country_id, region_id, district_id, ward_id, thumbnail_url, view_count, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: article_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_categories (id, name, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: article_article_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_article_categories (id, article_id, article_categories_id) FROM stdin;
\.


--
-- Data for Name: article_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_tags (id, name, name_code, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: article_article_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_article_tags (id, article_id, article_tags_id) FROM stdin;
\.


--
-- Data for Name: article_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_comment (id, user_id, article_id, content, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: article_reaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article_reaction (id, user_id, article_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: community_post_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post_categories (id, name, name_code, description, description_code, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: community_post; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post (id, user_id, category_id, title, content, thumbnail_url, view_count, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: community_post_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post_comment (id, user_id, post_id, content, parent_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: community_post_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post_tags (id, name, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: community_post_community_post_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post_community_post_tags (id, community_post_id, community_post_tag_id) FROM stdin;
\.


--
-- Data for Name: community_post_reaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.community_post_reaction (id, user_id, post_id, reaction_type, comment_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event_categories (id, name, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: organizer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizer (id, user_id, name, name_code, description, description_code, email, phone, website, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event (id, user_id, organizer_id, category_id, name, name_code, description, description_code, content, country_id, region_id, district_id, ward_id, thumbnail_url, view_count, start_time, start_date, end_date, price, max_attendees, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event_attendee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event_attendee (id, user_id, event_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event_sponsor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event_sponsor (id, organizer_id, event_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: food_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.food_categories (id, name, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: food; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.food (id, name, name_code, description, description_code, country_id, region_id, district_id, ward_id, category_id, thumbnail_url, price_min, price_max, popularity_score, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: location_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_categories (id, name, status, created_at, updated_at) FROM stdin;
1	Treking	t	2025-05-25 03:20:34.907107	\N
\.


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (id, name, name_code, description, description_code, latitude, longitude, geom, address, city, country_id, region_id, district_id, ward_id, category_id, thumbnail_url, price_min, price_max, popularity_score, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: media_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_category (id, name, description, status, created_date, updated_date) FROM stdin;
\.


--
-- Data for Name: media_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_type (id, name, description, status, created_date, updated_date) FROM stdin;
\.


--
-- Data for Name: media; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media (id, type_id, category_id, reference_id, reference_type, url, title, description, status, created_date, updated_date) FROM stdin;
\.


--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.password_reset_tokens (id, token, user_id, expires_at, is_used, created_at) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (id, name, description, code, created_at, updated_at) FROM stdin;
1	Edit Articles	Can edit article content	edit_articles	2025-05-22 16:08:44.959967	\N
2	role_create	\N	role:create	2025-05-24 12:43:28.986038	\N
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ratings (id, reference_id, reference_type, user_id, rating, comment, created_at) FROM stdin;
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
1	1
1	2
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Name: accommodation_rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accommodation_rooms_id_seq', 1, false);


--
-- Name: accommodations_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accommodations_categories_id_seq', 1, false);


--
-- Name: accommodations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accommodations_id_seq', 1, false);


--
-- Name: article_article_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_article_categories_id_seq', 1, false);


--
-- Name: article_article_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_article_tags_id_seq', 1, false);


--
-- Name: article_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_categories_id_seq', 1, false);


--
-- Name: article_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_comment_id_seq', 1, false);


--
-- Name: article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_id_seq', 1, false);


--
-- Name: article_reaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_reaction_id_seq', 1, false);


--
-- Name: article_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_tags_id_seq', 1, false);


--
-- Name: community_post_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_categories_id_seq', 1, false);


--
-- Name: community_post_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_comment_id_seq', 1, false);


--
-- Name: community_post_community_post_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_community_post_tags_id_seq', 1, false);


--
-- Name: community_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_id_seq', 1, false);


--
-- Name: community_post_reaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_reaction_id_seq', 1, false);


--
-- Name: community_post_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.community_post_tags_id_seq', 1, false);


--
-- Name: continents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.continents_id_seq', 8, true);


--
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.countries_id_seq', 583, true);


--
-- Name: districts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.districts_id_seq', 790, true);


--
-- Name: event_attendee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_attendee_id_seq', 1, false);


--
-- Name: event_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_categories_id_seq', 1, false);


--
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_id_seq', 1, false);


--
-- Name: event_sponsor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_sponsor_id_seq', 1, false);


--
-- Name: food_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_categories_id_seq', 1, false);


--
-- Name: food_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_id_seq', 1, false);


--
-- Name: location_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_categories_id_seq', 1, true);


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_id_seq', 1, false);


--
-- Name: media_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_category_id_seq', 1, false);


--
-- Name: media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_id_seq', 1, false);


--
-- Name: media_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_type_id_seq', 1, false);


--
-- Name: organizer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organizer_id_seq', 1, false);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, false);


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissions_id_seq', 2, true);


--
-- Name: ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ratings_id_seq', 1, false);


--
-- Name: regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.regions_id_seq', 126, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: wards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wards_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

