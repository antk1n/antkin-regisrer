-- tabelite kontroll
--select * from public."OsauhingAPP_osauhing_isikud" order by id
--select * from public."OsauhingAPP_osauhing" order by id
--select * from public."OsauhingAPP_isikud" order by id
--GO

-- delete koik info tabelites
DELETE from public."OsauhingAPP_osauhing_isikud";
DELETE from public."OsauhingAPP_osauhing";
DELETE from public."OsauhingAPP_isikud";
GO

-- varskenda loendurid tabelites
ALTER SEQUENCE public."OsauhingAPP_osauhing_isikud_id_seq" RESTART WITH 1;
ALTER SEQUENCE public."OsauhingAPP_osauhing_id_seq" RESTART WITH 1;
ALTER SEQUENCE public."OsauhingAPP_isikud_id_seq" RESTART WITH 1;
GO

-- tabelite populatsioon
--tabel isikud
INSERT INTO
    public."OsauhingAPP_isikud" (id,isikutyyp,isosauhing,nimi,perenimi,kood)
VALUES
    (1,	'J',	true,	'Beer Lovers OÜ',	null,	    '1234567'),
	(2,	'F',	false,	'Heli',	            'Kopter',	'49810020001'),
	(3,	'F',	false,	'Arnold',	        'Kopter',	'39810020002'),
	(4,	'J',	true,	'Veele OÜ',		     null,      '7894561'),
	(5,	'J',	true,	'OÜ Huvitavad Vaartused', null,	'9638527'),
	(6,	'F',	false,	'Timo',	            'Maasikas',	'37510070001'),
	(7,	'F',	false,	'Toomas',	        'Mets',	    '37010070002'),
	(8,	'F',	false,	'Artjom',	        'Oja',	    '37207070003'),
	(9,	'F',	false,	'Triin',	        'Anton',	'47407070004'),
	(10,'J',	true,	'Alati Nous OÜ',	null,	    '7418529'),
	(11,'F',	false,	'Tanel',	        'Tamm', 	'39205030001'),
	(12,'J',	false,	'Sopruse pst 5555 KÜ', null,	'8534917'),
	(13,'J',	true,	'Andrei Kiik OÜ',	null,   	'5687124'),
	(14,'F',	false,	'Andrei',	        'Kiik', 	'39512290009'),
	(15,'J',	true,	'Talu Oja OÜ',	    null,	    '5873614'),
	(16,'F',	false,	'Markus',	        'Oja',  	'39805020001'),
	(17,'F',	false,	'Margus',	        'Oja',  	'37009020002'),
	(18,'F',	false,	'Mart',	            'Oja',  	'39206020003'),
	(19,'F',	false,	'Merike',	        'Oja',	    '49606020004'),
	(20,'F',	false,	'Siim',	            'Pipp', 	'39106020005'),
	(21,'J',	true,	'Variku talu mesi OÜ',	null,	'1985117'),
	(22,'F',	false,	'Jaan',	            'Varik',	'35508150001'),
	(23,'J',	true,	'Head Lendu OÜ',    null,		'9852364'),
	(24,'J',	false,	'Swedish airlines',	null,   	'8753169'),
	(25,'J',	true,	'Anton Kink OÜ',	null,   	'1111111'),
	(26,'F',	false,	'Anton',	        'Kink',	    '39810020200'),
	(27,'F',	false,	'Maksim',	        'Kink', 	'37408140300'),
	(28,'J',	true,	'Halb liigutus',	null,   	'9988765'),
	(29,'J',    false,	'siim kikk FIE',	null,   	'9836412'),
	(30,'J',	true,	'123 pohjust',	    null,   	'2387695'),
	(31,'F',	false,	'Joseph',	        'Tamm', 	'38904310001'),
	(32,'J',	true,	'oü Laulupidu',	    null,   	'5555555'),
	(33,'J',	false,	'Lilla Tamm FIE',   null,		'8527435');
GO

--tabel osauhing
INSERT INTO
    public."OsauhingAPP_osauhing" (id,asutamisekp, kogukapital, isik_id)
VALUES
	(1,	'2023-07-29',	5000,	1),
	(2,	'2023-07-02',	4000,	4),
	(3,	'2023-05-09',	16000,	5),
	(4,	'2022-06-15',	10000,	10),
	(5,	'2019-10-29',	9100,	13),
	(6,	'2005-06-07',	13423,	15),
	(7,	'2023-07-03',	2500,	21),
	(8,	'2021-06-29',	200000,	23),
	(9,	'2019-06-04',	7000,	25),
	(10,'2023-07-12',	2500,	28),
	(11,'2019-07-16',	2500,	30),
	(12,'1993-06-22',	3501,	32);
GO

-- tabel osauhing_isikud
INSERT INTO
    public."OsauhingAPP_osauhing_isikud" (id,"osauhinguOsa", isasutaja, isik_id, osauhing_id)
VALUES
	(1,	2500,	true,	2,	1),
	(2,	2500,	true,	3,	1),
	(3,	4000,	true,	2,	2),
	(4,	5000,	true,	6,	3),
	(5,	5000,	true,	7,	3),
	(6,	5000,	true,	8,	3),
	(7,	1000,	false,	9,	3),
	(8,	2500,	true,	11,	4),
	(9,	7500,	false,	12,	4),
	(10,9100,	true,	14,	5),
	(11,100,	true,	16,	6),
	(12,5123,	true,	17,	6),
	(13,3000,	true,	18,	6),
	(14,200,	false,	19,	6),
	(15,5000,	false,	20,	6),
	(16,2500,	true,	22,	7),
	(17,200000,	true,	24,	8),
	(18,6000,	true,	26,	9),
	(19,1000,	false,	27,	9),
	(20,2500,	true,	29,	10),
	(21,2500,	true,	31,	11),
	(22,3501,	true,	33,	12);
	
	
