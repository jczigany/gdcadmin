-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2021. Feb 07. 12:36
-- Kiszolgáló verziója: 10.4.17-MariaDB
-- PHP verzió: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `gdcadmindb`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `jogcim`
--

CREATE TABLE `jogcim` (
  `id` int(11) NOT NULL,
  `jogcim` varchar(25) COLLATE utf8_hungarian_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

--
-- A tábla adatainak kiíratása `jogcim`
--

INSERT INTO `jogcim` (`id`, `jogcim`) VALUES
(1, 'Egyéb'),
(2, 'Tagdíj'),
(3, 'Ifjúsági tagdíj'),
(4, 'Bérlet'),
(5, 'Ifjúsági bérlet'),
(6, 'Napidíj'),
(7, 'Ifjúsági napidíj'),
(8, 'Adomány');

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `kassza`
--

CREATE TABLE `kassza` (
  `id` int(11) NOT NULL,
  `datum` date NOT NULL,
  `nyugta` int(11) NOT NULL DEFAULT 0,
  `befizeto` varchar(50) COLLATE utf8_hungarian_ci NOT NULL,
  `jogcim` varchar(30) COLLATE utf8_hungarian_ci NOT NULL,
  `ev` int(11) NOT NULL,
  `honap` int(11) NOT NULL,
  `osszeg` decimal(10,0) NOT NULL,
  `fizmod` varchar(10) COLLATE utf8_hungarian_ci NOT NULL DEFAULT 'Készpénz',
  `megjegyzes` varchar(100) COLLATE utf8_hungarian_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `vezeteknev` varchar(30) COLLATE utf8_hungarian_ci NOT NULL,
  `utonev` varchar(20) COLLATE utf8_hungarian_ci NOT NULL,
  `szuletesi_ido` date NOT NULL,
  `irszam` varchar(4) COLLATE utf8_hungarian_ci NOT NULL,
  `helyseg` varchar(25) COLLATE utf8_hungarian_ci NOT NULL,
  `cim` varchar(30) COLLATE utf8_hungarian_ci NOT NULL,
  `telefon` varchar(15) COLLATE utf8_hungarian_ci NOT NULL,
  `email` varchar(35) COLLATE utf8_hungarian_ci NOT NULL,
  `tagsag_kezdete` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;

--
-- A tábla adatainak kiíratása `members`
--

INSERT INTO `members` (`id`, `vezeteknev`, `utonev`, `szuletesi_ido`, `irszam`, `helyseg`, `cim`, `telefon`, `email`, `tagsag_kezdete`) VALUES
(1, 'Adame', 'Máté', '1994-08-09', '2600', 'Vác', 'Arató utca 4.', '+36309379724', 'adamejavelin@gmail.com', '2020-09-04'),
(2, 'Búzás', 'Zsolt', '1973-11-06', '2170', 'Aszód', 'Vörösmarty utca 25.', '+36304465069', 'zsoca736@gmail.com', '2020-09-04'),
(3, 'Cakó', 'Tamás', '1999-10-04', '2112', 'Veresegyház', 'Bánóczi utca 1.', '+36703946522', 'tomikaa24@gmail.com', '2020-10-10'),
(4, 'Czigány', 'Dávid', '1997-05-05', '2170', 'Aszód', 'Szőlő utca 16.', '+36303358881', 'devertarater@gmail.com', '2020-09-09'),
(5, 'Czigány', 'János', '1968-05-20', '2170', 'Aszód', 'Szőlő utca 16.', '+36703679791', 'jczigany59@gmail.com', '2020-06-29'),
(6, 'Dévai', 'Gábor', '0000-00-00', '2170', 'Aszód', 'Szőlő utca 8.', '+36202886548', 'devusgabi@gmail.com', '0000-00-00'),
(7, 'Gavló', 'Zoltán', '1963-01-21', '2112', 'Veresegyház', 'Szent István út 11', '+36303383966', 'gavlo.zoltan@gmail.com', '2020-09-11'),
(8, 'Guba', 'Ferenc', '1989-05-15', '2170', 'Aszód', 'Hunyadi utca 32.', '+36202968843', 'gzpainting16@gmail.com', '2020-06-29'),
(9, 'Gubáné Szikora', 'Tímea', '1993-06-25', '2170', 'Aszód', 'Hunyadi utca 32.', '+36202412291', 'szikora.timea0625@gmail.com', '2020-06-29'),
(10, 'Gulyás', 'Ádám', '1990-03-15', '2174', 'Verseg', 'Fő út 42.', '+36703852049', 'gulyasadam5@gmail.com', '2020-09-09'),
(11, 'Gulyás', 'Gábor', '1985-03-09', '2170', 'Verseg', 'Fő út 42.', '+36706702254', 'gulyasbogyo@gmail.com', '2020-09-09'),
(12, 'Gulyás', 'Jenő', '1964-07-29', '2174', 'Verseg', 'Fő út 42.', '+36704326412', '', '2020-09-09'),
(13, 'Hibó', 'Dana', '1999-03-03', '2170', 'Aszód', 'Szőlő utca 16/A', '+36203861261', 'angyalidana@gmail.com', '2020-11-10'),
(14, 'Kelemen', 'Tibor', '1972-09-19', '2173', 'Kartal', 'Császár út 121.', '+36706221075', 'degatibi1972@gmail.com', '2020-09-11'),
(15, 'Kolozs', 'Mónika', '1978-11-08', '2170', 'Aszód', 'Pesti út 2/4', '+36707799139', 'varjumonika@gmail.com', '2020-09-18'),
(16, 'Lados', 'Péter', '1976-07-13', '2173', 'Kartal', 'Orgona utca 40.', '+36707018164', '', '2020-09-26'),
(17, 'Lukács', 'Zsolt', '1970-03-06', '2170', 'Aszód', 'Szentkereszt út 9.', '+36702125907', 'lukacs.zsolt.mester@gmail.com', '2020-06-29'),
(18, 'Nagy', 'Gábor Dániel', '1990-02-02', '2100', 'Gödöllő', 'Erzsébet krt. 19.', '+36702948694', 'nagy_gabor_daniel@windowslive.com', '2020-09-11'),
(19, 'Rektenwald', 'Máté', '1996-01-29', '2173', 'Kartal', 'Ady Endre utca 10.', '+36209376256', 'rektenwald96@gmail.com', '2020-09-04'),
(20, 'Romhányi', 'Renáta', '1978-12-06', '2170', 'Aszód', 'Szőlő utca 16.', '+36704545791', 'reniromhanyi@gmail.com', '2020-06-29'),
(21, 'Szikora', 'Tibor', '1964-04-26', '2170', 'Aszód', 'Hunyadi utca 32.', '+36707731349', 'szikora.tibor64@gmail.com', '2020-09-03'),
(22, 'Tóth', 'Csaba', '1980-03-16', '2170', 'Aszód', 'Mosolygó utca 1.', '+36706081619', 'tcsking01@freemail.hu', '2020-10-17'),
(23, 'Urbán', 'Gábor', '1977-08-07', '2173', 'Kartal', 'Orgona utca 8.', '+36302741284', 'urbangabor@invitel.hu', '2020-09-25'),
(24, 'Urr', 'László', '1973-06-19', '2170', 'Aszód', 'Bethlen Gábor utca 61.', '+36203826078', 'mesterurr@citromail.hu', '2020-06-29'),
(25, 'Varga', 'Zoltán', '1969-04-05', '2173', 'Kartal', 'Kodály Zoltán utca 9/A', '+36304022031', 'vozo.hu@gmail.com', '2020-09-25'),
(26, 'Varjú', 'Botond', '2010-04-07', '2170', 'Aszód', 'Pesti út 2/4', '+36707799139', 'varjumonika@gmail.com', '2020-09-18'),
(27, 'Varjú', 'Nándor', '2008-03-20', '2170', 'Aszód', 'Pesti út 2/4', '+36707799139', 'varjumonika@gmail.com', '2020-09-18');

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `jogcim`
--
ALTER TABLE `jogcim`
  ADD PRIMARY KEY (`id`);

--
-- A tábla indexei `kassza`
--
ALTER TABLE `kassza`
  ADD PRIMARY KEY (`id`);

--
-- A tábla indexei `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `jogcim`
--
ALTER TABLE `jogcim`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT a táblához `kassza`
--
ALTER TABLE `kassza`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT a táblához `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
