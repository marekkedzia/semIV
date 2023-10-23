-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Cze 19, 2023 at 12:18 PM
-- Wersja serwera: 10.4.28-MariaDB
-- Wersja PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `szkola 2023 lista3 pon np 13 kedzia`
--

DELIMITER $$
--
-- Procedury
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `z1-A01-uczniowie-z-klas-I-III` ()   SELECT Uczniowie.Nazwisko, Uczniowie.Imie, Uczniowie.IdU AS Id, Klasy.Symbol AS Klasa FROM Klasy JOIN Uczniowie ON Klasy.Symbol = Uczniowie.KlasaU WHERE (Klasy.Symbol LIKE 'I%' AND Klasy.Symbol NOT LIKE 'IV%') OR Klasy.Symbol LIKE 'II%' OR Klasy.Symbol LIKE 'III%' ORDER BY Uczniowie.Nazwisko, Uczniowie.Imie, Uczniowie.IdU$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z10-A05-nauczyciele-o-stazu-powyzej` (IN `staż` INT(255))   SELECT Nauczyciele.IdN, Nauczyciele.Nazwisko, Nauczyciele.Imie, Nauczyciele.DZatr, 
       TIMESTAMPDIFF(YEAR, Nauczyciele.DZatr, CURDATE()) AS Staz
FROM Nauczyciele
WHERE TIMESTAMPDIFF(YEAR, Nauczyciele.DZatr, CURDATE()) > staż
ORDER BY Nauczyciele.Nazwisko, Nauczyciele.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z2-A04-zatrudnieni-po-1-marca` ()   SELECT Nauczyciele.IdN, Nauczyciele.Nazwisko, Nauczyciele.Imie, Nauczyciele.DZatr, Nauczyciele.DUr, Nauczyciele.Plec, Nauczyciele.Pensja, Nauczyciele.Pensum, Nauczyciele.Telefon, Nauczyciele.Premia FROM Nauczyciele WHERE Nauczyciele.DZatr >= '2020-03-01' ORDER BY Nauczyciele.Nazwisko, Nauczyciele.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z3-A07a-uczniowie-malejaco-ocenami` ()   SELECT Uczniowie.Nazwisko, Uczniowie.Imie, Przedmioty.NazwaP, Oceny.Ocena FROM Uczniowie JOIN Oceny ON Uczniowie.IdU = Oceny.IdU JOIN Przedmioty ON Przedmioty.IdP = Oceny.IdP ORDER BY Oceny.Ocena DESC, Uczniowie.Nazwisko, Uczniowie.Imie$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z4-A11-uczniowie-z-miast` ()   SELECT Uczniowie.IdU, Uczniowie.Nazwisko, Uczniowie.Imie, Miasta.NazwaM
FROM Miasta 
INNER JOIN Uczniowie ON Miasta.IdM = Uczniowie.Miasto
WHERE Miasta.NazwaM = 'Brzeg' 
   OR Miasta.NazwaM = 'Brzeg Dolny' 
   OR Miasta.NazwaM = 'Opole'$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z5-A14-liczba-uczniów-z-miast` ()   SELECT Miasta.NazwaM, Count(Uczniowie.Miasto) AS PoliczOfMiasto FROM Miasta LEFT JOIN Uczniowie ON Miasta.IdM = Uczniowie.Miasto GROUP BY Miasta.NazwaM$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z6-A20-ilosć-przedmiotów-z-oceną` ()   SELECT Uczniowie.Nazwisko, Uczniowie.Imie, Count(Oceny.IdU) AS IlośćOcen FROM Uczniowie INNER JOIN Oceny ON Uczniowie.IdU = Oceny.IdU INNER JOIN Przedmioty ON Przedmioty.IdP = Oceny.IdP GROUP BY Uczniowie.Nazwisko, Uczniowie.Imie ORDER BY Count(Oceny.IdU) DESC$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z7-A28-staż` ()   SELECT Nauczyciele.IdN, Nauczyciele.Nazwisko, Nauczyciele.Imie, COALESCE(DATEDIFF(CURRENT_DATE, DZatr), 0) AS `Staż w dniach`, COALESCE(TIMESTAMPDIFF(MONTH, DZatr, CURRENT_DATE), 0) AS `Staż w miesiącach`, COALESCE(TIMESTAMPDIFF(YEAR, DZatr, CURRENT_DATE), 0) AS `Staż w latach` FROM Nauczyciele ORDER BY COALESCE(TIMESTAMPDIFF(YEAR, DZatr, CURRENT_DATE), 0) DESC$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z8-A27-nauczyciele-bez-wychowawstwa` ()   SELECT Nauczyciele.Nazwisko, Nauczyciele.Imie
FROM Nauczyciele 
LEFT JOIN Klasy ON Nauczyciele.IdN = Klasy.Wych
WHERE Klasy.Symbol IS NULL$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `z9-A02-uczniowie-z-miast-B-P-z-klas-II` ()   SELECT Uczniowie.IdU, Uczniowie.Nazwisko, Uczniowie.Imie, Uczniowie.DUr, Uczniowie.Plec, Uczniowie.KlasaU, Uczniowie.Miasto FROM Uczniowie INNER JOIN Klasy ON Klasy.Symbol = Uczniowie.KlasaU INNER JOIN Miasta ON Miasta.IdM = Uczniowie.Miasto WHERE Uczniowie.KlasaU LIKE 'II%' AND Uczniowie.KlasaU NOT LIKE 'III%' AND Miasta.NazwaM REGEXP '^[B-P].*' ORDER BY Uczniowie.Nazwisko, Uczniowie.Imie, Uczniowie.IdU$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `klasy`
--

CREATE TABLE `klasy` (
  `Symbol` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Profil` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Wych` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `klasy`
--

INSERT INTO `klasy` (`Symbol`, `Profil`, `Wych`) VALUES
('Ia', 'Fizyczny', 2),
('Ig', 'Humanistyczny', 16),
('Ih', 'Ogólny', 15),
('IId', 'Ogólny', NULL),
('IIg', 'Muzyczny', 2),
('IIIa', 'Geograficzny', 8),
('IIIc', 'Wojskowy', 3),
('Ik', 'Historyczny', 17),
('Ip', 'Językowy', NULL),
('IVa', 'Humanistyczny', 4),
('Va', 'Ogólny', NULL);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `miasta`
--

CREATE TABLE `miasta` (
  `IdM` int(11) NOT NULL,
  `NazwaM` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `miasta`
--

INSERT INTO `miasta` (`IdM`, `NazwaM`) VALUES
(1, 'Żmigród'),
(2, 'Warszawa'),
(3, 'Wrocław'),
(4, 'Świebodzice'),
(5, 'Strzegom'),
(6, 'Olszany'),
(7, 'Wałbrzych'),
(8, 'Oława'),
(9, 'Londyn'),
(10, 'Świdnica'),
(11, 'Opole'),
(12, 'Trzcinówek'),
(13, 'Kraków'),
(14, 'Praga'),
(15, 'Rzym'),
(16, 'Kędzierzyn-Koźle'),
(18, 'Brzeg Dolny'),
(19, 'Brzeg');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `nauczyciele`
--

CREATE TABLE `nauczyciele` (
  `IdN` int(11) NOT NULL,
  `Nazwisko` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Imie` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `DZatr` date DEFAULT NULL,
  `DUr` date DEFAULT NULL,
  `Plec` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Pensja` double DEFAULT NULL,
  `Pensum` int(11) DEFAULT NULL,
  `Telefon` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Premia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `nauczyciele`
--

INSERT INTO `nauczyciele` (`IdN`, `Nazwisko`, `Imie`, `DZatr`, `DUr`, `Plec`, `Pensja`, `Pensum`, `Telefon`, `Premia`) VALUES
(1, 'Nowak', 'Jan', '2023-03-13', NULL, 'M', 10000, 300, '123456789', 0),
(2, 'Kowalski', 'Tomasz', '2023-03-08', '2000-09-12', 'M', 5000.51, 390, NULL, 100),
(3, 'Wojaczek', 'Honorata', '2020-03-13', '1978-09-01', 'K', 4500, 30, '987654321', 50),
(4, 'Zatorska', 'Katarzyna', '2005-06-13', NULL, 'K', 0, 0, '111111111', 0),
(8, 'Żmuda', 'Joanna', '2023-03-13', NULL, 'K', 0, 60, NULL, 10),
(9, 'Żmuda', 'Adam', '2023-03-13', '1981-01-01', 'M', 0, 0, NULL, 0),
(10, 'Kowalski', 'Tomasz', '2023-03-26', '1999-10-15', 'M', 11000.39, 45, '686898111', 5),
(11, 'Ziółkowska', 'Eleonora', '2022-03-26', NULL, 'K', 0, 0, NULL, 0),
(12, 'Nowak', 'Elżbieta', '2023-03-26', '1976-02-13', 'K', 5000, 90, '530478284', 500),
(13, 'Terlikowkski', 'Łukasz', '2021-03-13', '2000-04-01', 'M', 0, 0, NULL, 0),
(14, 'Marek', 'Joanna', '2023-01-26', '1930-06-02', 'K', 13000.66, 300, '841358991', 10),
(15, 'Kiraga', 'Elżbieta', '2023-03-26', NULL, 'K', 0, 0, '147258369', 0),
(16, 'Płytowski', 'Janusz', '2023-03-26', NULL, NULL, 0, 0, NULL, 0),
(17, 'Niedolny', 'Filip', '2005-03-26', '1973-01-01', 'M', 0, 0, NULL, 0),
(18, 'Lepper', 'Kornel', '2023-03-28', NULL, NULL, 0, 0, NULL, 0),
(19, 'Naren', 'Rajesh', '2023-03-26', '1984-04-04', 'M', 3300, 420, '999666777', 100),
(20, 'Tijar', 'Rajesh', '2023-04-20', '1990-04-01', 'M', 0, 0, NULL, 0),
(21, 'Kowalski', 'Jan', '2023-04-20', '1901-01-01', 'M', 12000, 30, '123456789', 1000),
(22, 'Kwiatkowski', 'Karol', '2023-04-24', '1990-05-02', 'M', 10000.87, 0, NULL, 0),
(23, 'Kwiatkowski', 'Karol', '2023-04-24', '2000-01-01', 'M', 0, 0, NULL, 0);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `oceny`
--

CREATE TABLE `oceny` (
  `IdU` int(11) NOT NULL,
  `IdP` int(11) NOT NULL,
  `Ocena` double NOT NULL,
  `DataO` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `oceny`
--

INSERT INTO `oceny` (`IdU`, `IdP`, `Ocena`, `DataO`) VALUES
(3, 8, 2, '2023-03-26'),
(4, 7, 4, '2023-03-26'),
(7, 5, 3, '2023-03-26'),
(11, 5, 4.5, '2023-03-13'),
(13, 2, 4.5, '2023-05-07'),
(13, 4, 4, '2023-03-13'),
(13, 5, 5, '2023-05-07'),
(19, 8, 5, '2023-04-20'),
(22, 7, 2, NULL),
(28, 7, 4, '2023-03-26'),
(29, 5, 5, '2023-03-26'),
(35, 7, 4.5, '2023-03-26'),
(37, 5, 4.5, NULL),
(39, 4, 2, '2023-04-20'),
(39, 8, 3, '2023-03-26'),
(40, 5, 2, '2023-03-26'),
(42, 4, 4.5, '2023-03-26'),
(42, 9, 4, '2023-04-20'),
(45, 4, 5, '2023-04-20'),
(45, 8, 2, '2023-03-26'),
(48, 7, 4, '2023-03-26'),
(48, 8, 5, NULL),
(50, 4, 4, '2023-03-26'),
(53, 6, 2, '2023-03-26'),
(54, 7, 2, NULL),
(56, 6, 2, '2023-04-20'),
(56, 8, 3, '2023-03-26'),
(58, 1, 2, '2023-03-26'),
(58, 2, 4, NULL),
(58, 3, 3, '2023-04-20'),
(58, 4, 3, '2023-03-27'),
(58, 5, 3, '2023-03-26'),
(58, 6, 5, '2023-04-20'),
(58, 7, 4, '2023-03-26'),
(58, 8, 3, '2023-03-26'),
(58, 9, 2, '2023-04-20');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `przedmioty`
--

CREATE TABLE `przedmioty` (
  `IdP` int(11) NOT NULL,
  `NazwaP` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `przedmioty`
--

INSERT INTO `przedmioty` (`IdP`, `NazwaP`) VALUES
(1, 'Przyroda'),
(2, 'W-F'),
(3, 'Język Angielski'),
(4, 'Fizyka'),
(5, 'Matematyka'),
(6, 'Język Polski'),
(7, 'Historia'),
(8, 'WoS'),
(9, 'Godzina Wychowawcza'),
(10, 'Język Niemiecki');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `uczniowie`
--

CREATE TABLE `uczniowie` (
  `IdU` int(11) NOT NULL,
  `Nazwisko` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Imie` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `DUr` date DEFAULT NULL,
  `Plec` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `KlasaU` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Miasto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `uczniowie`
--

INSERT INTO `uczniowie` (`IdU`, `Nazwisko`, `Imie`, `DUr`, `Plec`, `KlasaU`, `Miasto`) VALUES
(1, 'Kowalsky', 'John', '1990-04-13', 'M', 'IIIc', 4),
(2, 'Kowalska', 'Angelika', '2000-04-14', 'K', 'Ia', 5),
(3, 'Kowalska', 'Angelika', '2001-09-15', 'K', 'IIIc', 18),
(4, 'Kowalska', 'Justyna', '1999-12-31', 'K', 'Ia', 3),
(5, 'Aaron', 'Paul', '2003-11-11', 'M', 'Ik', 5),
(6, 'Zapolska', 'Gabriela', '2004-12-10', 'K', 'IIg', 3),
(7, 'Żeromski', 'Stefan', '1997-11-18', 'M', NULL, 8),
(10, 'Smudziński', 'Krzysztof', '2000-05-14', 'M', 'IIg', 6),
(11, 'Nowakowska', 'Martyna', '2002-02-12', 'K', 'IVa', 4),
(12, 'Jackowska', 'Daria', '2003-12-07', 'K', 'Ik', 19),
(13, 'Rożek', 'Marcel', '1999-05-04', 'M', 'Ik', 11),
(14, 'Wawryszczuk', 'Kasjan', '2002-08-25', 'M', 'IVa', 4),
(15, 'Kazek', 'Kacper', '2003-06-06', 'M', 'IVa', 8),
(16, 'Bagazja', 'Szymon', '2004-10-17', 'M', NULL, NULL),
(17, 'Mosiężna', 'Emilia', '2005-03-02', 'K', NULL, NULL),
(18, 'Kowalczyk', 'Mikołaj', NULL, NULL, 'IIIc', NULL),
(19, 'Gęsioła', 'Daniel', '2002-11-28', NULL, NULL, 14),
(20, 'Młynarczyk', 'Wiktor', '2008-02-05', 'M', 'Ip', 14),
(21, 'Młynarkiewicz', 'Wiktoria', '2001-02-01', 'K', 'IVa', NULL),
(22, 'Nosal', 'Kacper', '2001-01-01', 'M', NULL, NULL),
(23, 'Zatorska', 'Katarzyna', '2001-01-07', 'K', 'IIg', NULL),
(24, 'Stanowska', 'Katarzyna', NULL, NULL, 'Ik', NULL),
(25, 'Lubomirska', 'Krystyna', '1999-12-12', 'K', 'Ip', 19),
(26, 'Lubomirski', 'Dawid', '1999-12-12', 'M', 'Ip', 9),
(27, 'Lubomirski', 'Stanisław', '1999-12-31', 'M', 'Ik', 3),
(28, 'Habibi', 'Imran', '2006-08-14', 'M', 'IId', 2),
(29, 'Artem', 'Valerii', '2001-09-17', 'M', NULL, NULL),
(30, 'Wszędobylski', 'Kornel', NULL, 'M', 'IId', 13),
(31, 'Marek', 'Monika', NULL, 'K', NULL, NULL),
(32, 'Kołakowska', 'Aleksandra', '1999-12-03', 'K', 'IIIa', 10),
(33, 'Rutecki', 'Jakub', NULL, NULL, NULL, NULL),
(34, 'Strzelecki', 'Zbigniew', '1998-08-06', 'M', 'Ia', 4),
(35, 'Najman', 'Marcin', '2003-03-03', NULL, NULL, NULL),
(36, 'Kędzierska', 'Weronika', '2000-06-01', 'K', 'IId', 6),
(37, 'Kędzierski', 'Jakub', '2008-08-08', 'M', 'IIg', 7),
(38, 'Przemyślany', 'Przemysław', '2004-09-01', 'M', 'IIg', NULL),
(39, 'Kuternoga', 'Katarzyna', '2005-06-15', 'K', 'Ig', 13),
(40, 'Chivay', 'Zoltan', '2001-07-12', 'M', 'Ik', 9),
(41, 'Bard', 'Jaskier', NULL, 'M', 'Ip', NULL),
(42, 'Riv', 'Geralt', '2001-04-14', 'M', 'Ip', NULL),
(43, 'Merigold', 'Triss', '2004-05-06', 'K', 'IIIa', 1),
(44, 'Roheltz', 'Regis', '1999-03-15', 'M', 'Ik', NULL),
(45, 'Calleah', 'Cahir', NULL, NULL, 'IIIa', NULL),
(46, 'Rianon', 'Ciri', NULL, 'K', 'IId', 12),
(47, 'Fiona', 'Stefania', '2001-05-27', 'K', 'Ig', NULL),
(48, 'Sierzkowska', 'Milena', NULL, 'K', NULL, NULL),
(49, 'Armata', 'Szczepan', '2005-12-14', 'M', 'IId', 14),
(50, 'Armata', 'Jagoda', '2004-03-18', NULL, NULL, 11),
(51, 'Potrzeba', 'Jagoda', '1999-09-14', 'K', 'IId', 13),
(52, 'Mus', 'Celina', '1998-12-14', 'K', 'Ip', 12),
(53, 'Johnson', 'Ligma', '2001-02-03', 'M', 'IVa', 3),
(54, 'Jenkins', 'Leroy', '2001-04-15', 'M', 'IIIc', 11),
(55, 'Korybut', 'Łukasz', '2001-06-04', 'M', 'Ik', 7),
(56, 'Wiśniowieski', 'Michał', '2003-03-03', 'M', NULL, NULL),
(57, 'Barlay', 'Mink', NULL, NULL, NULL, NULL),
(58, 'Monostone', 'Albert', NULL, NULL, NULL, NULL),
(59, 'Manstain', 'Erich', '2001-08-19', 'M', 'Ip', 10);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `uczy`
--

CREATE TABLE `uczy` (
  `IdN` int(11) NOT NULL,
  `IdP` int(11) NOT NULL,
  `IleGodz` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `uczy`
--

INSERT INTO `uczy` (`IdN`, `IdP`, `IleGodz`) VALUES
(1, 2, 20),
(2, 6, 5),
(3, 7, 20),
(3, 8, 20),
(3, 9, 10),
(4, 5, 30),
(4, 6, 10),
(4, 9, 2),
(8, 4, 30),
(10, 4, 20),
(10, 8, 5),
(11, 4, 1),
(11, 6, 10),
(12, 7, 20),
(13, 7, 10),
(14, 1, 15),
(14, 9, 5),
(15, 6, 20),
(16, 8, 30),
(17, 7, 30),
(18, 2, 20),
(18, 9, 4),
(19, 3, 4),
(19, 5, 40),
(20, 1, 2),
(20, 2, 2),
(20, 3, 2),
(20, 4, 2),
(20, 5, 2),
(20, 6, 2),
(20, 7, 2),
(20, 8, 2),
(20, 9, 2),
(20, 10, 2);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `klasy`
--
ALTER TABLE `klasy`
  ADD PRIMARY KEY (`Symbol`);

--
-- Indeksy dla tabeli `miasta`
--
ALTER TABLE `miasta`
  ADD PRIMARY KEY (`IdM`);

--
-- Indeksy dla tabeli `nauczyciele`
--
ALTER TABLE `nauczyciele`
  ADD PRIMARY KEY (`IdN`);

--
-- Indeksy dla tabeli `oceny`
--
ALTER TABLE `oceny`
  ADD PRIMARY KEY (`IdU`,`IdP`);

--
-- Indeksy dla tabeli `przedmioty`
--
ALTER TABLE `przedmioty`
  ADD PRIMARY KEY (`IdP`);

--
-- Indeksy dla tabeli `uczniowie`
--
ALTER TABLE `uczniowie`
  ADD PRIMARY KEY (`IdU`);

--
-- Indeksy dla tabeli `uczy`
--
ALTER TABLE `uczy`
  ADD PRIMARY KEY (`IdN`,`IdP`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `miasta`
--
ALTER TABLE `miasta`
  MODIFY `IdM` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `nauczyciele`
--
ALTER TABLE `nauczyciele`
  MODIFY `IdN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `przedmioty`
--
ALTER TABLE `przedmioty`
  MODIFY `IdP` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `uczniowie`
--
ALTER TABLE `uczniowie`
  MODIFY `IdU` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
