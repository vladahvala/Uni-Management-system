-- 1. Створення таблиць

CREATE TABLE Людина (
    Паспорт VARCHAR(20) NOT NULL,
    ПІБ VARCHAR(100) NOT NULL,
    PRIMARY KEY (Паспорт)
);

CREATE TABLE Студент (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Людини
    Курс_навчання INT NOT NULL,
    Форма_навчання VARCHAR(50) NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Студент_Людина FOREIGN KEY (Паспорт)
        REFERENCES Людина(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Член_персоналу (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Людини
    Зарплата DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Член_персоналу_Людина FOREIGN KEY (Паспорт)
        REFERENCES Людина(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Член_деканату (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Член персоналу
    Посада VARCHAR(50) NOT NULL,
    Службовий_телефон VARCHAR(20) NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Член_деканату_Член_персоналу FOREIGN KEY (Паспорт)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Викладач (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Член персоналу
    Предмет VARCHAR(50) NOT NULL,
    Науковий_ступінь VARCHAR(50) NOT NULL,
    Стаж_викладання FLOAT NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Викладач_Член_персоналу FOREIGN KEY (Паспорт)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Член_неакад_персоналу (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Член персоналу
    Посада VARCHAR(50) NOT NULL,
    Відділ_роботи VARCHAR(50) NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Член_неакад_персоналу_Член_персоналу FOREIGN KEY (Паспорт)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Директор (
    Паспорт VARCHAR(20) NOT NULL,  -- ключ з Член персоналу
    Кабінет INT NOT NULL,
    Дата_призначення DATE NOT NULL,
    PRIMARY KEY (Паспорт),
    CONSTRAINT fk_Директор_Член_персоналу FOREIGN KEY (Паспорт)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Група (
    Номер INT NOT NULL,  
    Кількість_студентів INT NOT NULL,
    Спеціальність VARCHAR(100) NOT NULL,
    PRIMARY KEY (Номер)
);

CREATE TABLE Університет (
    ID INT NOT NULL,  
    Назва VARCHAR(70) NOT NULL,
    Адреса VARCHAR(80) NOT NULL,
    Тип VARCHAR(20) NOT NULL,
    Рік_заснування YEAR NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Кабінет (
    Номер INT NOT NULL,  
    Поверх INT NOT NULL,
    Кількість_місць INT NOT NULL,
    Тип VARCHAR(50) NOT NULL,
    ID_університету INT NOT NULL,  -- зовнішній ключ на Університет
    PRIMARY KEY (Номер),
    CONSTRAINT fk_Кабінет_Університет FOREIGN KEY (ID_університету)
        REFERENCES Університет(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Захід (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Тип VARCHAR(50) NOT NULL,
    Тривалість INT NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Захід_Кабінет FOREIGN KEY (Номер_кабінету)
        REFERENCES Кабінет(Номер)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Засідання (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Кількість_учасників INT NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Засідання_Захід FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Захід(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Культурна_подія (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Тематика VARCHAR(255) NOT NULL,
    Програма VARCHAR(255) NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Культурна_подія_Захід FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Захід(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Пара (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Предмет VARCHAR(50) NOT NULL,
    Тривалість INT NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Пара_Кабінет FOREIGN KEY (Номер_кабінету)
        REFERENCES Кабінет(Номер)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Лекція (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Розглянутий_матеріал VARCHAR(255) NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Лекція_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Практика (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Кількість_учасників INT NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Практика_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Екзамен (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Кількість_перевіряючих INT NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Екзамен_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Консультація (
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    Питання VARCHAR(100) NOT NULL,
    PRIMARY KEY (Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Консультація_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



-- 2. Додавання зв’язків між таблицями

-- Зв'язки сутності Студент

-- Додавання зовнішнього ключа на Групу (M:1 "належить")
ALTER TABLE Студент
ADD COLUMN Номер_групи INT NOT NULL;

ALTER TABLE Студент
ADD CONSTRAINT FK_Студент_Група
FOREIGN KEY (Номер_групи)
REFERENCES Група(Номер)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Додавання зовнішнього ключа на Університет (M:1 "навчається")
ALTER TABLE Студент
ADD COLUMN ID_університету INT NOT NULL,
ADD CONSTRAINT fk_Студент_Університет
FOREIGN KEY (ID_університету)
REFERENCES Університет(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Проміжна таблиця для M:N "присутній" (студент - пара)
CREATE TABLE Відвідування (
    Паспорт VARCHAR(20) NOT NULL,
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    PRIMARY KEY (Паспорт, Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Відвідування_Студент FOREIGN KEY (Паспорт)
        REFERENCES Студент(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Відвідування_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- Зв'язки сутності Член персоналу

-- Додавання зовнішнього ключа на Університет (M:1 "працює")
ALTER TABLE Член_персоналу
ADD COLUMN ID_університету INT NOT NULL,
ADD CONSTRAINT FK_Член_персоналу_Університет
FOREIGN KEY (ID_університету)
REFERENCES Університет(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- Додавання зовнішнього ключа на Кабінет (M:1 "закріплений за")
ALTER TABLE Член_персоналу
ADD COLUMN Номер_кабінету INT,
ADD CONSTRAINT FK_Член_персоналу_Кабінет
FOREIGN KEY (Номер_кабінету)
REFERENCES Кабінет(Номер)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- Проміжна таблиця для M:N "відвідує" (член персоналу - захід)
CREATE TABLE Відвідування_заходів (
    Паспорт VARCHAR(20) NOT NULL,
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    PRIMARY KEY (Паспорт, Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Відвідування_персонал FOREIGN KEY (Паспорт)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Відвідування_Захід FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Захід(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Проміжна таблиця для M:N "має дружні стосунки" (член персоналу - член персоналу)
CREATE TABLE Дружні_стосунки (
    Паспорт1 VARCHAR(20) NOT NULL,
    Паспорт2 VARCHAR(20) NOT NULL,
    PRIMARY KEY (Паспорт1, Паспорт2),
    CONSTRAINT fk_Дружні_стосунки_Член1 FOREIGN KEY (Паспорт1)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Дружні_стосунки_Член2 FOREIGN KEY (Паспорт2)
        REFERENCES Член_персоналу(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_Дружні_стосунки UNIQUE (Паспорт2, Паспорт1)
);


-- Зв'язки сутності Викладач

-- Додавання зв'язку 1:M "курує" (викладач -> група)
ALTER TABLE Група
ADD COLUMN Паспорт_викладача VARCHAR(20),
ADD CONSTRAINT FK_Група_Викладач
FOREIGN KEY (Паспорт_викладача)
REFERENCES Викладач(Паспорт)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- Проміжна таблиця для M:N "проводить" (викладач - пара)
CREATE TABLE Проведення_пар (
    Паспорт_викладача VARCHAR(20) NOT NULL,
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    PRIMARY KEY (Паспорт_викладача, Дата, Час_початку, Номер_кабінету),
    CONSTRAINT fk_Проведення_Викладач FOREIGN KEY (Паспорт_викладача)
        REFERENCES Викладач(Паспорт)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_Проведення_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Зв'язки сутності Директор

-- Додавання зв'язку 1:1 "керує" (директор -> університет)
ALTER TABLE Директор
ADD COLUMN ID_університету INT NOT NULL,
ADD CONSTRAINT FK_Університет_Директор
FOREIGN KEY (ID_університету)
REFERENCES Університет(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;


-- Зв'язки сутності Група
-- 2. Додавання зовнішнього ключа на Університет (N:1 "існує в")
ALTER TABLE Група
ADD COLUMN ID_університету INT NOT NULL,
ADD CONSTRAINT FK_Група_Університет
FOREIGN KEY (ID_університету)
REFERENCES Університет(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 3. Проміжна таблиця для M:N "проводиться для" (група - пара)
CREATE TABLE Група_Пара (
    Номер_групи INT NOT NULL,
    Дата DATE NOT NULL,
    Час_початку TIME NOT NULL,
    Номер_кабінету INT NOT NULL,
    PRIMARY KEY (Номер_групи, Дата, Час_початку, Номер_кабінету),
    CONSTRAINT FK_Група_Пара_Група FOREIGN KEY (Номер_групи)
        REFERENCES Група(Номер)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_Група_Пара_Пара FOREIGN KEY (Дата, Час_початку, Номер_кабінету)
        REFERENCES Пара(Дата, Час_початку, Номер_кабінету)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



-- 3. Заповнення таблиць даними

-- Люди 
INSERT INTO Людина (Паспорт, ПІБ) VALUES
('AA123456', 'Іваненко Іван Іванович'),
('BB987654', 'Петренко Петро Петрович'),
('CC456789', 'Сидоренко Оксана Михайлівна'),
('DD654321', 'Коваленко Марія Андріївна'),
('EE112233', 'Ткаченко Сергій Вікторович'),
('GG123123', 'Кравченко Олег Ігорович'),
('HH234234', 'Мельник Наталія Вікторівна'),
('II345345', 'Бондаренко Юрій Сергійович'),
('JJ456456', 'Савченко Лариса Петрівна'),
('KK567567', 'Шевченко Андрій Іванович'),
('LL678678', 'Кузьменко Ольга Павлівна'),
('MM789789', 'Гончаренко Віктор Олександрович'),
('NN890890', 'Дмитренко Світлана Ігорівна'),
('OO901901', 'Романенко Павло Володимирович'),
('PP556677', 'Левченко Олександр Віталійович'),
('QQ223344', 'Мороз Наталія Сергіївна'),
('RR667788', 'Козак Ігор Павлович'),
('TT112233', 'Гнатюк Валерій Олексійович'),
('SS778899', 'Савчук Ірина Петрівна'),
('ZZ334455', 'Федоренко Олег Андрійович');

SELECT * FROM Член_персоналу;
-- Студенти
INSERT INTO Студент (Паспорт, Курс_навчання, Форма_навчання, Номер_групи, ID_університету) VALUES
('AA123456', 1, 'денна', 101, 1),
('DD654321', 1, 'денна', 104, 1), 
('BB987654', 2, 'денна', 102, 2),
('EE112233', 2, 'заочна', 105, 2),  
('CC456789', 3, 'заочна', 103, 3);

-- Викладачі
INSERT INTO Член_персоналу (Паспорт, Зарплата, ID_університету, Номер_кабінету) VALUES
('GG123123', 18000.00, 1, 201),
('HH234234', 19000.00, 1, 202),
('II345345', 17000.00, 2, 301),
('JJ456456', 16000.00, 2, 302);

-- Члени деканату
INSERT INTO Член_персоналу (Паспорт, Зарплата, ID_університету, Номер_кабінету) VALUES
('KK567567', 20000.00, 1, 203),
('LL678678', 21000.00, 1, 204),
('MM789789', 19500.00, 2, 303),
('NN890890', 20500.00, 2, 304);

-- Члени неакадем. персоналу
INSERT INTO Член_персоналу (Паспорт, Зарплата, ID_університету, Номер_кабінету) VALUES
('OO901901', 12000.00, 1, NULL),
('PP556677', 13000.00, 1, NULL),
('QQ223344', 12500.00, 2, NULL),
('RR667788', 13500.00, 2, NULL);

-- Директори
INSERT INTO Член_персоналу (Паспорт, Зарплата, ID_університету, Номер_кабінету) VALUES
('TT112233', 25000.00, 1, 101),
('SS778899', 26000.00, 2, 201),
('ZZ334455', 27000.00, 3, 301);

-- Викладачі
INSERT INTO Викладач (Паспорт, Предмет, Науковий_ступінь, Стаж_викладання) VALUES
('GG123123', 'Математика', 'Кандидат наук', 5),
('HH234234', 'Фізика', 'Доктор наук', 10),
('II345345', 'Хімія', 'Кандидат наук', 7),
('JJ456456', 'Інформатика', 'Доктор наук', 12);

-- Члени деканату
INSERT INTO Член_деканату (Паспорт, Посада, Службовий_телефон) VALUES
('KK567567', 'Заступник декана', '123-45-67'),
('LL678678', 'Секретар деканату', '123-45-68'),
('MM789789', 'Куратор факультету', '123-45-69'),
('NN890890', 'Методист', '123-45-70');

-- Члени неакадемічного персоналу 
INSERT INTO Член_неакад_персоналу (Паспорт, Посада, Відділ_роботи) VALUES
('OO901901', 'Прибиральник', 'Технічний відділ'),
('PP556677', 'Охоронець', 'Служба безпеки'),
('QQ223344', 'Прибиральник', 'Технічний відділ'),
('RR667788', 'Охоронець', 'Служба безпеки');

-- Директори 
INSERT INTO Директор (Паспорт, Кабінет, Дата_призначення, ID_університету) VALUES
('TT112233', 101, '2023-09-01', 1),
('SS778899', 201, '2022-09-01', 2),
('ZZ334455', 301, '2024-01-15', 3);


-- Групи
INSERT INTO Група (Номер, Кількість_студентів, Спеціальність, ID_університету) VALUES
(101, 10, 'Математика', 1),
(102, 12, 'Фізика', 2),
(103, 15, 'Хімія', 3),
(104, 8, 'Фізика', 1),
(105, 9, 'Біотехнології', 2);

-- Університети
INSERT INTO Університет (ID, Назва, Адреса, Тип, Рік_заснування)
VALUES
(1, 'Київський національний університет', 'м. Київ, вул. Володимирська, 60', 'державний', 1901),
(2, 'Львівський національний університет', 'м. Львів, вул. Університетська, 1', 'державний', 1929),
(3, 'Харківський національний університет', 'м. Харків, вул. Пушкінська, 10', 'державний', 1980);

-- Кабінети
INSERT INTO Кабінет (Номер, Поверх, Кількість_місць, Тип, ID_університету)
VALUES
(101, 1, 12, 'Засідання', 1),
(102, 1, 30, 'Лекції', 1),
(201, 2, 25, 'Лекції', 2),
(202, 2, 20, 'Практичні заняття', 2),
(301, 3, 30, 'Лекції', 3),
(302, 3, 20, 'Практичні заняття', 3),
(203, 2, 12, 'Засідання', 1),
(204, 2, 25, 'Лекції', 1),
(303, 3, 15, 'Засідання', 2),
(304, 3, 20, 'Практичні заняття', 2);

-- Захід
INSERT INTO Захід (Дата, Час_початку, Номер_кабінету, Тип, Тривалість) VALUES
('2025-10-23', '10:00:00', 101, 'Засідання', 90),
('2025-10-24', '14:00:00', 102, 'Засідання', 120),
('2025-10-25', '16:00:00', 201, 'Культурна подія', 45),
('2025-10-26', '11:00:00', 202, 'Культурна подія', 180);

-- Засідання
INSERT INTO Засідання (Дата, Час_початку, Номер_кабінету, Кількість_учасників) VALUES
('2025-10-23', '10:00:00', 101, 8),
('2025-10-24', '14:00:00', 102, 5);

-- Культурні події
INSERT INTO Культурна_подія (Дата, Час_початку, Номер_кабінету, Тематика, Програма) VALUES
('2025-10-25', '16:00:00', 201, 'Концерт класичної музики', 'Виконання симфоній Бетховена'),
('2025-10-26', '11:00:00', 202, 'Вистава студентського театру', 'Комедія за Шекспіром');

-- Пара
INSERT INTO Пара (Дата, Час_початку, Номер_кабінету, Предмет, Тривалість) VALUES
('2025-10-23', '09:00:00', 101, 'Математика', 90),
('2025-10-23', '11:00:00', 102, 'Фізика', 120),
('2025-10-24', '10:00:00', 201, 'Хімія', 90),
('2025-10-24', '13:00:00', 202, 'Інформатика', 60),
('2025-10-25', '09:00:00', 101, 'Математика', 90),
('2025-10-25', '11:00:00', 102, 'Фізика', 60);

-- Лекції
INSERT INTO Лекція (Дата, Час_початку, Номер_кабінету, Розглянутий_матеріал) VALUES
('2025-10-23', '09:00:00', 101, 'Тригонометричні функції'),
('2025-10-23', '11:00:00', 102, 'Закони Ньютона');

-- Практики
INSERT INTO Практика (Дата, Час_початку, Номер_кабінету, Кількість_учасників) VALUES
('2025-10-24', '10:00:00', 201, 15),
('2025-10-24', '13:00:00', 202, 12);

-- Екзамени
INSERT INTO Екзамен (Дата, Час_початку, Номер_кабінету, Кількість_перевіряючих) VALUES
('2025-10-25', '09:00:00', 101, 2);

-- Консультації
INSERT INTO Консультація (Дата, Час_початку, Номер_кабінету, Питання) VALUES
('2025-10-25', '11:00:00', 102, 'Питання по фізиці');

-- Група_Пара 
INSERT INTO Група_Пара (Номер_групи, Дата, Час_початку, Номер_кабінету) VALUES
(101, '2025-10-23', '09:00:00', 101),
(104, '2025-10-24', '13:00:00', 202),
(102, '2025-10-23', '11:00:00', 102),
(105, '2025-10-24', '10:00:00', 201),
(101, '2025-10-25', '09:00:00', 101),
(102, '2025-10-25', '11:00:00', 102);

-- Проведення_пар
INSERT INTO Проведення_пар (Паспорт_викладача, Дата, Час_початку, Номер_кабінету) VALUES
('GG123123', '2025-10-23', '09:00:00', 101),
('HH234234', '2025-10-23', '11:00:00', 102),
('II345345', '2025-10-24', '10:00:00', 201),
('HH234234', '2025-10-24', '13:00:00', 202),
('GG123123', '2025-10-25', '09:00:00', 101),
('HH234234', '2025-10-25', '11:00:00', 102);

-- Дружні_стосунки 
INSERT INTO Дружні_стосунки (Паспорт1, Паспорт2) VALUES
('GG123123', 'HH234234'),
('II345345', 'JJ456456'),
('KK567567', 'LL678678'),
('MM789789', 'NN890890');

-- Відвідування_заходів 
INSERT INTO Відвідування_заходів (Паспорт, Дата, Час_початку, Номер_кабінету) VALUES
('KK567567', '2025-10-23', '10:00:00', 101),
('LL678678', '2025-10-24', '14:00:00', 102),
('MM789789', '2025-10-25', '16:00:00', 201),
('NN890890', '2025-10-26', '11:00:00', 202);

-- Відвідування 
INSERT INTO Відвідування (Паспорт, Дата, Час_початку, Номер_кабінету) VALUES
('AA123456', '2025-10-23', '09:00:00', 101),
('DD654321', '2025-10-24', '13:00:00', 202),
('BB987654', '2025-10-23', '11:00:00', 102),
('EE112233', '2025-10-24', '10:00:00', 201),
('AA123456', '2025-10-25', '09:00:00', 101),
('BB987654', '2025-10-25', '11:00:00', 102);


-- 4. Механізм soft delete

-- Студент
ALTER TABLE Студент
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE Студент
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

DROP PROCEDURE IF EXISTS DeleteStudent;

CREATE PROCEDURE DeleteStudent(IN pPassport VARCHAR(20), IN pUser VARCHAR(100))
BEGIN
    UPDATE Студент
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;

DROP PROCEDURE IF EXISTS RestoreStudent;

CREATE PROCEDURE RestoreStudent(IN pPassport VARCHAR(20), IN pUser VARCHAR(100))
BEGIN
    UPDATE Студент
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;

DROP PROCEDURE IF EXISTS AddStudent;
CREATE PROCEDURE AddStudent(
    IN pPassport VARCHAR(20),
    IN pPIB VARCHAR(255),
    IN pGroupNumber INT,
    IN pCourse INT,
    IN pForm VARCHAR(50),
    IN pUniversityID INT,
    IN pUser VARCHAR(100)
)
BEGIN
    -- 1. Додаємо людину
    INSERT INTO Людина (Паспорт, ПІБ)
    VALUES (pPassport, pPIB);

    -- 2. Додаємо студента
    INSERT INTO Студент (Паспорт, Курс_навчання, Форма_навчання, Номер_групи, ID_університету, UpdatedBy)
    VALUES (pPassport, pCourse, pForm, pGroupNumber, pUniversityID, pUser);
END;


DROP PROCEDURE IF EXISTS UpdateStudent;
CREATE PROCEDURE UpdateStudent(
    IN pPassport VARCHAR(20),
    IN pCourse INT,
    IN pForm VARCHAR(50),
    IN pGroupNumber INT,
    IN pUser VARCHAR(100)
)
BEGIN
    UPDATE Студент
    SET Курс_навчання = pCourse,
        Форма_навчання = pForm,
        Номер_групи = pGroupNumber,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;


DROP PROCEDURE IF EXISTS GetAllStudents;
CREATE PROCEDURE GetAllStudents()
BEGIN
    SELECT * FROM StudentDetails;
END;

DROP PROCEDURE IF EXISTS GetStudentByPassport;
CREATE PROCEDURE GetStudentByPassport(IN pPassport VARCHAR(20))
BEGIN
    SELECT * FROM StudentDetails WHERE Паспорт = pPassport;
END;


CREATE OR REPLACE VIEW ActiveStudents AS
SELECT 
    s.Паспорт,
    l.ПІБ,
    s.Курс_навчання,
    s.Форма_навчання,
    s.Номер_групи,
    u.Назва AS Університет
FROM Студент s
JOIN Людина l ON s.Паспорт = l.Паспорт
JOIN Університет u ON s.ID_університету = u.ID
WHERE s.IsDeleted = 0;

CREATE OR REPLACE VIEW StudentDetails AS 
SELECT 
    s.Паспорт, 
    l.ПІБ, 
    s.Курс_навчання, 
    s.Форма_навчання, 
    g.Номер AS Група, 
    u.ID AS Університет_ID, 
    u.Назва AS Університет 
FROM Студент s 
JOIN Людина l ON s.Паспорт = l.Паспорт 
JOIN Група g ON s.Номер_групи = g.Номер 
JOIN Університет u ON s.ID_університету = u.ID;


-- Член персоналу

-- ---------------------- Додаткові колонки ----------------------
ALTER TABLE Член_персоналу
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0,
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

-- ---------------------- Видалення ----------------------
DROP PROCEDURE IF EXISTS DeleteStaff;
CREATE PROCEDURE DeleteStaff(IN pPassport VARCHAR(20), IN pUser VARCHAR(100))
BEGIN
    UPDATE Член_персоналу
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;

-- ---------------------- Відновлення ----------------------
DROP PROCEDURE IF EXISTS RestoreStaff;
CREATE PROCEDURE RestoreStaff(IN pPassport VARCHAR(20), IN pUser VARCHAR(100))
BEGIN
    UPDATE Член_персоналу
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;

-- ---------------------- Додавання ----------------------
DROP PROCEDURE IF EXISTS AddStaff;
CREATE PROCEDURE AddStaff(
    IN pPassport VARCHAR(20),
    IN pPIB VARCHAR(255),
    IN pSalary DECIMAL(10,2),
    IN pUniversityID INT,
    IN pUser VARCHAR(100)
)
BEGIN
    -- 1. Додаємо людину
    INSERT INTO Людина (Паспорт, ПІБ)
    VALUES (pPassport, pPIB);

    -- 2. Додаємо члена персоналу
    INSERT INTO Член_персоналу (Паспорт, Зарплата, ID_університету, UpdatedBy)
    VALUES (pPassport, pSalary, pUniversityID, pUser);
END;

-- ---------------------- Оновлення ----------------------
DROP PROCEDURE IF EXISTS UpdateStaff;
CREATE PROCEDURE UpdateStaff(
    IN pPassport VARCHAR(20),
    IN pSalary DECIMAL(10,2),
    IN pUniversityID INT,
    IN pUser VARCHAR(100)
)
BEGIN
    UPDATE Член_персоналу
    SET Зарплата = pSalary,
        ID_університету = pUniversityID,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Паспорт = pPassport;
END;

-- ---------------------- Отримання ----------------------
DROP PROCEDURE IF EXISTS GetAllStaff;
CREATE PROCEDURE GetAllStaff()
BEGIN
    SELECT * FROM ActiveStaff;
END;

DROP PROCEDURE IF EXISTS GetStaffByPassport;
CREATE PROCEDURE GetStaffByPassport(IN pPassport VARCHAR(20))
BEGIN
    SELECT * FROM ActiveStaff WHERE Паспорт = pPassport;
END;

-- ---------------------- VIEW для активних членів персоналу ----------------------
CREATE OR REPLACE VIEW ActiveStaff AS
SELECT 
    s.Паспорт,
    l.ПІБ,
    s.Зарплата,
    g.Номер AS Кабінет, 
    u.Назва AS Університет
FROM Член_персоналу s
JOIN Людина l ON s.Паспорт = l.Паспорт
JOIN Кабінет g ON s.Номер_кабінету = g.Номер 
JOIN Університет u ON s.ID_університету = u.ID
WHERE s.IsDeleted = 0;

CREATE OR REPLACE VIEW StaffDetails AS 
SELECT 
    s.Паспорт, 
    l.ПІБ, 
    s.Зарплата, 
    g.Номер AS Кабінет, 
    u.ID AS Університет_ID, 
    u.Назва AS Університет 
FROM Член_персоналу s 
JOIN Людина l ON s.Паспорт = l.Паспорт 
JOIN Кабінет g ON s.Номер_кабінету = g.Номер 
JOIN Університет u ON s.ID_університету = u.ID;



-- Група
ALTER TABLE Група
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE Група
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

DROP PROCEDURE IF EXISTS DeleteGroup;

CREATE PROCEDURE DeleteGroup(IN pGroupNumber INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Група
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Номер = pGroupNumber;
END;


DROP PROCEDURE IF EXISTS RestoreGroup;

CREATE PROCEDURE RestoreGroup(IN pGroupNumber INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Група
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Номер = pGroupNumber;
END;

-- ---------------------- Отримання ----------------------
DROP PROCEDURE IF EXISTS GetAllGroups;
CREATE PROCEDURE GetAllGroups()
BEGIN
    SELECT * FROM ActiveGroups;
END;

-- Додавання групи
DROP PROCEDURE IF EXISTS AddGroup;
CREATE PROCEDURE AddGroup(
    IN pNumber INT,
    IN pStudentCount INT,
    IN pSpecialty VARCHAR(100),
    IN pUniversityID INT,
    IN pUser VARCHAR(100)
)
BEGIN
    INSERT INTO Група (Номер, Кількість_студентів, Спеціальність, ID_університету, UpdatedBy)
    VALUES (pNumber, pStudentCount, pSpecialty, pUniversityID, pUser);
END;

-- Оновлення групи
DROP PROCEDURE IF EXISTS UpdateGroup;
CREATE PROCEDURE UpdateGroup(
    IN pNumber INT,
    IN pStudentCount INT,
    IN pSpecialty VARCHAR(100),
    IN pUniversityID INT,
    IN pUser VARCHAR(100)
)
BEGIN
    UPDATE Група
    SET Кількість_студентів = pStudentCount,
        Спеціальність = pSpecialty,
        ID_університету = pUniversityID,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Номер = pNumber;
END;

DROP PROCEDURE IF EXISTS GetGroupByNumber;
CREATE PROCEDURE GetGroupByNumber(IN pNum INT)
BEGIN
    SELECT * FROM GroupDetails WHERE Номер = pNum;
END;

CREATE OR REPLACE VIEW ActiveGroups AS
SELECT 
    g.Номер,
    g.Кількість_студентів,
    g.Спеціальність,
    u.ID AS Університет_ID,
    u.Назва AS Університет,
    g.UpdatedAt,
    g.UpdatedBy
FROM Група g
JOIN Університет u ON g.ID_університету = u.ID
WHERE g.IsDeleted = 0;

CREATE OR REPLACE VIEW GroupDetails AS
SELECT 
    g.Номер,
    g.Кількість_студентів,
    g.Спеціальність,
    u.ID AS Університет_ID,
    u.Назва AS Університет,
    v.Паспорт,
    l.ПІБ AS Викладач,
    g.UpdatedAt,
    g.UpdatedBy
FROM Група g
JOIN Університет u ON g.ID_університету = u.ID
LEFT JOIN Викладач v ON g.Паспорт_викладача = v.Паспорт
LEFT JOIN Людина l ON v.Паспорт = l.Паспорт
WHERE g.IsDeleted = 0;



-- Кабінет
ALTER TABLE Кабінет
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE Кабінет
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

DROP PROCEDURE IF EXISTS DeleteCabinet;

CREATE PROCEDURE DeleteCabinet(IN pCabinetNumber INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Кабінет
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Номер = pCabinetNumber;
END;


DROP PROCEDURE IF EXISTS RestoreCabinet;

CREATE PROCEDURE RestoreCabinet(IN pCabinetNumber INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Кабінет
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Номер = pCabinetNumber;
END;


CREATE VIEW ActiveCabinets AS
SELECT *
FROM Кабінет
WHERE IsDeleted = 0;


-- Захід
ALTER TABLE Захід
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE Захід
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

DROP PROCEDURE IF EXISTS DeleteEvent;

CREATE PROCEDURE DeleteEvent(IN pDate DATE, IN pTime TIME, IN pCabinet INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Захід
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Дата = pDate
      AND Час_початку = pTime
      AND Номер_кабінету = pCabinet;
END;

DROP PROCEDURE IF EXISTS RestoreEvent;

CREATE PROCEDURE RestoreEvent(IN pDate DATE, IN pTime TIME, IN pCabinet INT, IN pUser VARCHAR(100))
BEGIN
    UPDATE Захід
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Дата = pDate
      AND Час_початку = pTime
      AND Номер_кабінету = pCabinet;
END;

CREATE VIEW ActiveEvents AS
SELECT *
FROM Захід
WHERE IsDeleted = 0;


-- Пара
ALTER TABLE Пара
ADD COLUMN IsDeleted TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE Пара
ADD COLUMN UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN UpdatedBy VARCHAR(100) NULL;

DROP PROCEDURE IF EXISTS DeleteClass;

CREATE PROCEDURE DeleteClass(
    IN pDate DATE,
    IN pTime TIME,
    IN pCabinet INT,
    IN pUser VARCHAR(100)
)
BEGIN
    UPDATE Пара
    SET IsDeleted = 1,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Дата = pDate
      AND Час_початку = pTime
      AND Номер_кабінету = pCabinet;
END;

DROP PROCEDURE IF EXISTS RestoreClass;

CREATE PROCEDURE RestoreClass(
    IN pDate DATE,
    IN pTime TIME,
    IN pCabinet INT,
    IN pUser VARCHAR(100)
)
BEGIN
    UPDATE Пара
    SET IsDeleted = 0,
        UpdatedAt = NOW(),
        UpdatedBy = pUser
    WHERE Дата = pDate
      AND Час_початку = pTime
      AND Номер_кабінету = pCabinet;
END;

CREATE VIEW ActiveClasses AS
SELECT *
FROM Пара
WHERE IsDeleted = 0;


-- 5. Triggers

-- перевіряє зайнятість кабінету для пари
CREATE TRIGGER CheckCabinetAvailability
BEFORE INSERT ON Пара
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM Пара
        WHERE Номер_кабінету = NEW.Номер_кабінету
          AND Дата = NEW.Дата
          AND NEW.Час_початку < ADDTIME(Час_початку, SEC_TO_TIME(TIME_TO_SEC(Тривалість)*60))
          AND ADDTIME(NEW.Час_початку, SEC_TO_TIME(TIME_TO_SEC(NEW.Тривалість)*60)) > Час_початку
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Кабінет зайнятий на цей час';
    END IF;
END;

-- перевіряє зайнятість кабінету для заходу 
CREATE TRIGGER CheckCabinetAvailability_event
BEFORE INSERT ON Захід
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM Захід
        WHERE Номер_кабінету = NEW.Номер_кабінету
          AND Дата = NEW.Дата
          AND NEW.Час_початку < ADDTIME(Час_початку, SEC_TO_TIME(TIME_TO_SEC(Тривалість)*60))
          AND ADDTIME(NEW.Час_початку, SEC_TO_TIME(TIME_TO_SEC(NEW.Тривалість)*60)) > Час_початку
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Кабінет зайнятий на цей час';
    END IF;
END;

-- перевіряє курс студента (від 1 до 4)
CREATE TRIGGER StudyingYearCheck
BEFORE INSERT ON Студент
FOR EACH ROW
BEGIN
    IF NEW.Курс_навчання < 1 OR NEW.Курс_навчання > 4 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Курс навчання може бути лише від 1 до 4!';
    END IF;
END;

-- перевіряє, чи існує група, до якої додається студент
CREATE TRIGGER CheckActiveGroupBeforeInsert
BEFORE INSERT ON Студент
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Група
        WHERE Номер = NEW.Номер_групи
          AND IsDeleted = 0
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати студента: група не існує або розпущена.';
    END IF;
END;

-- перевіряє, чи існує університет, до якого додається студент
CREATE TRIGGER CheckUniBeforeInsert
BEFORE INSERT ON Студент
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Університет
        WHERE ID = NEW.ID_університету
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати студента: університет не існує або не доданий до таблиці.';
    END IF;
END;

-- перевіряє чи зарплата члена персоналу > min
CREATE TRIGGER PaymentCheck
BEFORE INSERT ON Член_персоналу
FOR EACH ROW
BEGIN
    IF NEW.Зарплата < 8000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Зарплата не може бути нижчою за мінімальну!';
    END IF;
END;

-- перевіряє чи існує кабінет, який вводиться для члена персоналу
CREATE TRIGGER CabinetCheck
BEFORE INSERT ON Член_персоналу
FOR EACH ROW
BEGIN
    IF NEW.Номер_кабінету IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1
            FROM Кабінет
            WHERE Номер_кабінету = NEW.Номер_кабінету
              AND ID_університету = NEW.ID_університету
              AND IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Вказаний кабінет не існує, неактивний або не належить цьому університету';
        END IF;
    END IF;
END;

-- перевіряє кількість студентів у групі
CREATE TRIGGER StudentNumCheck
BEFORE INSERT ON Група
FOR EACH ROW
BEGIN
    IF NEW.Кількість_студентів < 1 OR NEW.Кількість_студентів > 45 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Некоректно введена кількість студентів! Має бути від 1 до 45.';
    END IF;
END;

-- перевіряє чи існує викладач, який курує групу
CREATE TRIGGER CuratorCheck
BEFORE INSERT ON Група
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Викладач
        WHERE Паспорт = NEW.Паспорт_викладача
            AND ID_університету = NEW.ID_університету
            AND IsDeleted = 0
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Вказаний викладач не існує, звільнився або не належить цьому університету';
    END IF;
END;

-- перевіряє поверх, наявність університету і кількість місць кабінету
CREATE TRIGGER CabinetInfoCheck
BEFORE INSERT ON Кабінет
FOR EACH ROW
BEGIN
    DECLARE uni_count INT;

    -- Перевіряємо, чи існує університет
    SELECT COUNT(*) INTO uni_count
    FROM Університет
    WHERE ID = NEW.ID_університету;

    IF NEW.Кількість_місць < 30 
       OR NEW.Поверх < 1 
       OR NEW.Поверх > 5
       OR uni_count = 0
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Некоректно введена інформація про кабінет! Кількість місць - мінімум 30, поверхи від 1 до 5, університет має існувати.';
    END IF;
END;

-- перевіряє типу заходу 
CREATE TRIGGER EventTypeCheck
BEFORE INSERT ON Захід
FOR EACH ROW
BEGIN
    IF LOWER(NEW.Тип) != 'засідання' AND LOWER(NEW.Тип) != 'культурна подія' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Некоректно введений тип заходу!';
    END IF;
END;

-- перед додаванням нової культурної події переконуємося, що захід має відповідний тип
CREATE TRIGGER CulturalEventTypeCheck
BEFORE INSERT ON Культурна_подія
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Захід
        WHERE Дата = NEW.Дата
          AND Час_початку = NEW.Час_початку
          AND Номер_кабінету = NEW.Номер_кабінету
          AND LOWER(Тип) = 'культурна подія'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати культурну подію: відповідний захід має бути типу "Культурна подія"';
    END IF;
END;

-- перед додаванням нового засідання переконуємося, що захід має відповідний тип
CREATE TRIGGER ConferenceTypeCheck
BEFORE INSERT ON Засідання
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Захід
        WHERE Дата = NEW.Дата
          AND Час_початку = NEW.Час_початку
          AND Номер_кабінету = NEW.Номер_кабінету
          AND LOWER(Тип) = 'засідання'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати засідання: відповідний захід має бути типу "Засідання"';
    END IF;
END;

-- перевіряє, що директор належить до університету, який він керує
CREATE TRIGGER CheckDirectorUniversity
BEFORE INSERT ON Директор
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Член_персоналу
        WHERE Паспорт = NEW.Паспорт
          AND ID_університету = NEW.ID_університету
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати директора: він не належить до цього університету';
    END IF;
END;

-- перевіряє, що викладач, що проводить пару, належить до того ж університету
CREATE TRIGGER CheckTeacherForLesson
BEFORE INSERT ON Проведення_пар
FOR EACH ROW
BEGIN
    DECLARE uni_id INT;

    -- Дізнаємося університет через кабінет
    SELECT ID_університету INTO uni_id
    FROM Пара
    JOIN Кабінет ON Пара.Номер_кабінету = Кабінет.Номер
    WHERE Пара.Дата = NEW.Дата
      AND Пара.Час_початку = NEW.Час_початку
      AND Пара.Номер_кабінету = NEW.Номер_кабінету;

    -- Перевіряємо, чи викладач належить до цього університету
    IF NOT EXISTS (
        SELECT 1
        FROM Викладач
        WHERE Паспорт = NEW.Паспорт_викладача
          AND ID_університету = uni_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неможливо додати викладача: він не належить до університету, де проводиться пара';
    END IF;
END;

-- перевіряє, чи викаладач не веде кілька пар одночасно
CREATE TRIGGER CheckTeacherDoubleBooking
BEFORE INSERT ON Проведення_пар
FOR EACH ROW
BEGIN
    DECLARE new_start TIME;
    DECLARE new_end TIME;

    -- отримуємо час початку та кінець нової пари
    SELECT Час_початку, ADDTIME(Час_початку, SEC_TO_TIME(TIME_TO_SEC(Тривалість)*60))
    INTO new_start, new_end
    FROM Пара
    WHERE Дата = NEW.Дата
      AND Час_початку = NEW.Час_початку
      AND Номер_кабінету = NEW.Номер_кабінету;

    -- перевіряємо, чи викладач вже веде іншу пару в цей час
    IF EXISTS (
        SELECT 1
        FROM Проведення_пар pp
        JOIN Пара p ON pp.Дата = p.Дата 
                   AND pp.Час_початку = p.Час_початку 
                   AND pp.Номер_кабінету = p.Номер_кабінету
        WHERE pp.Паспорт_викладача = NEW.Паспорт_викладача
          AND NEW.Дата = pp.Дата
          AND new_start < ADDTIME(p.Час_початку, SEC_TO_TIME(TIME_TO_SEC(p.Тривалість)*60))
          AND new_end > p.Час_початку
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Цей викладач уже веде іншу пару в цей час!';
    END IF;
END;

-- перевірка чи дружні стосунки не з самим собою
CREATE TRIGGER CheckFriendshipSelf
BEFORE INSERT ON Дружні_стосунки
FOR EACH ROW
BEGIN
    IF NEW.Паспорт1 = NEW.Паспорт2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Не можна додати дружні стосунки з самим собою.';
    END IF;
END;

-- неможливо soft delete викладача, якщо він куратор групи або проводить пари
CREATE TRIGGER CheckTeacherSoftDelete
BEFORE UPDATE ON Член_персоналу
FOR EACH ROW
BEGIN
    -- перевіряємо, що оновлюється викладач
    IF EXISTS (SELECT 1 FROM Викладач WHERE Паспорт = OLD.Паспорт) THEN
        IF NEW.IsDeleted = 1 AND OLD.IsDeleted = 0 THEN
            -- Перевірка кураторства
            IF EXISTS (
                SELECT 1
                FROM Група
                WHERE Паспорт_викладача = OLD.Паспорт
                  AND IsDeleted = 0
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Неможливо видалити викладача: він куратор групи';
            END IF;

            -- Перевірка проведення пар
            IF EXISTS (
                SELECT 1
                FROM Проведення_пар
                WHERE Паспорт_викладача = OLD.Паспорт
                  AND IsDeleted = 0
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Неможливо видалити викладача: він проводить пари';
            END IF;
        END IF;
    END IF;
END;

-- не можна видаляти групу, якщо є активні студенти/викладач/пари
CREATE TRIGGER CheckGroupSoftDelete
BEFORE UPDATE ON Група
FOR EACH ROW
BEGIN
    IF NEW.IsDeleted = 1 AND OLD.IsDeleted = 0 THEN
        -- Перевірка студентів
        IF EXISTS (
            SELECT 1
            FROM Студент
            WHERE ID_групи = OLD.Номер
              AND IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Неможливо видалити групу: є активні студенти';
        END IF;

        -- Перевірка викладача
        IF EXISTS (
            SELECT 1
            FROM Група g
            JOIN Член_персоналу cp ON g.Паспорт_викладача = cp.Паспорт
            WHERE g.Номер = OLD.Номер
              AND cp.IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Неможливо видалити групу: у групи є активний викладач';
        END IF;

        -- Перевірка пар
        IF EXISTS (
            SELECT 1
            FROM Пара
            WHERE ID_групи = OLD.Номер
              AND IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Неможливо видалити групу: є активні пари';
        END IF;
    END IF;
END;

-- не можна видаляти кабінет, якщо є активні пари/заходи 
CREATE TRIGGER CheckCabinetSoftDelete
BEFORE UPDATE ON Кабінет
FOR EACH ROW
BEGIN
    IF NEW.IsDeleted = 1 AND OLD.IsDeleted = 0 THEN

        -- Перевірка пар
        IF EXISTS (
            SELECT 1
            FROM Пара
            WHERE Номер_кабінету = OLD.Номер
              AND IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Неможливо видалити кабінет: є активні пари';
        END IF;

        -- Перевірка заходів
        IF EXISTS (
            SELECT 1
            FROM Захід
            WHERE Номер_кабінету = OLD.Номер
            AND IsDeleted = 0
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Неможливо видалити кабінет: є активні заходи';
        END IF;

    END IF;
END;


-- 6. User-Defined Functions

-- повертає кількість студентів у групі
CREATE FUNCTION CountStudentsInGroup(group_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE student_count INT;

    SELECT COUNT(*)
    INTO student_count
    FROM Студент
    WHERE Номер_групи = group_id;

    RETURN student_count;
END;

-- повертає кількість студентів певного курсу і університету
CREATE FUNCTION StudentsInCourse(course_number INT, uni_id INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE student_list TEXT;

    SELECT GROUP_CONCAT(l.ПІБ SEPARATOR ', ')
    INTO student_list
    FROM Студент s
    JOIN Людина l ON s.Паспорт = l.Паспорт
    WHERE s.Курс_навчання = course_number
      AND s.ID_університету = uni_id;

    RETURN student_list;
END;

-- повертає список груп, які курує конкретний викладач
CREATE FUNCTION GroupsOfTeacher(teacher_passport VARCHAR(20))
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE group_list TEXT;

    SELECT GROUP_CONCAT(g.Номер SEPARATOR ', ')
    INTO group_list
    FROM Група g
    WHERE g.Паспорт_викладача = teacher_passport;

    RETURN group_list;
END;

-- Припустимо, у нас є група з номером 101, і викладач з паспортом 'AB123456'
UPDATE Група
SET Паспорт_викладача = 'GG123123'
WHERE Номер = 101;

-- повертає список пар, які проводить конкретний викладач
CREATE FUNCTION LessonsOfTeacher(teacher_passport VARCHAR(20))
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE lessons_list TEXT;

    SELECT GROUP_CONCAT(
             CONCAT('Дата: ', Дата, ', Час: ', Час_початку, ', Кабінет: ', Номер_кабінету)
             SEPARATOR '; '
           )
    INTO lessons_list
    FROM Проведення_пар
    WHERE Паспорт_викладача = teacher_passport;

    RETURN lessons_list;
END;

-- повертає список заходів певного типу у певний проміжок часу
CREATE FUNCTION EventsByTypeRange(
    type VARCHAR(50),
    date_start DATE,
    date_end DATE
)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE events_list TEXT;

    SELECT GROUP_CONCAT(
               CONCAT('Дата: ', Дата, ', Час: ', Час_початку, ', Кабінет: ', Номер_кабінету)
               SEPARATOR '; '
           )
    INTO events_list
    FROM Захід
    WHERE LOWER(Тип) = LOWER(type)
      AND Дата BETWEEN date_start AND date_end;

    RETURN events_list;
END;

-- Список персоналу університету
CREATE FUNCTION StaffByUniversity(uni_id INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE staff_list TEXT;

    SELECT GROUP_CONCAT(CONCAT('Паспорт: ', Паспорт, ', ПІБ: ', ПІБ)
             SEPARATOR '; ')
    INTO staff_list
    FROM Член_персоналу cp
    JOIN Людина l ON cp.Паспорт = l.Паспорт
    WHERE cp.ID_університету = uni_id;

    RETURN staff_list;
END;

-- середня зарплата по університету
CREATE FUNCTION AverageSalary(uni_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE avg_salary DECIMAL(10,2);

    SELECT AVG(Зарплата)
    INTO avg_salary
    FROM Член_персоналу
    WHERE ID_університету = uni_id;

    RETURN avg_salary;
END;


-- 6. Views

-- інформація про студента (студент + група + університет)
CREATE OR REPLACE VIEW StudentDetails AS
SELECT 
    s.Паспорт,
    l.ПІБ,              
    s.Курс_навчання,
    s.Форма_навчання,
    g.Номер AS Група,
    u.ID AS Університет_ID,
    u.Назва AS Університет
FROM Студент s
JOIN Людина l ON s.Паспорт = l.Паспорт
JOIN Група g ON s.Номер_групи = g.Номер
JOIN Університет u ON s.ID_університету = u.ID;

-- інформація про члена персоналу (член персоналу + кабінет + університет)
CREATE OR REPLACE VIEW StaffDetails AS
SELECT 
    m.Паспорт,
    l.ПІБ,              
    m.Зарплата,
    c.Номер AS Кабінет,
    u.ID AS Університет_ID,
    u.Назва AS Університет
FROM Член_персоналу m
JOIN Людина l ON m.Паспорт = l.Паспорт
JOIN Кабінет c ON m.Номер_кабінету = c.Номер
JOIN Університет u ON m.ID_університету = u.ID;

-- інформація про пару (пара + група + викладач + кабінет)
CREATE OR REPLACE VIEW ClassSchedule AS
SELECT 
    p.Дата,
    p.Час_початку,
    p.Номер_кабінету,
    p.Предмет,
    p.Тривалість,
    g.Номер AS Група,
    t.Паспорт AS Викладач,
    l.ПІБ AS Викладач_ПІБ,
    u.Назва AS Університет
FROM Пара p
JOIN Група_Пара gp 
    ON p.Дата = gp.Дата 
    AND p.Час_початку = gp.Час_початку 
    AND p.Номер_кабінету = gp.Номер_кабінету
JOIN Група g 
    ON gp.Номер_групи = g.Номер
JOIN Член_персоналу t 
    ON g.Паспорт_викладача = t.Паспорт
JOIN Людина l 
    ON t.Паспорт = l.Паспорт
JOIN Університет u
    ON g.ID_університету = u.ID;


-- інформація про захід (захід + відвідувачі )
CREATE OR REPLACE VIEW EventAttendence AS
SELECT 
    z.Дата,
    z.Час_початку,
    z.Номер_кабінету,
    z.Тип,
    z.Тривалість,
    t.Паспорт AS Відвідувач_Паспорт,
    l.ПІБ AS Відвідувач_ПІБ
FROM Захід z
JOIN Відвідування_заходів zv
    ON z.Дата = zv.Дата 
    AND z.Час_початку = zv.Час_початку 
    AND z.Номер_кабінету = zv.Номер_кабінету
JOIN Член_персоналу t 
    ON zv.Паспорт = t.Паспорт
JOIN Людина l
    ON t.Паспорт = l.Паспорт;


-- 6. Indexes

-- Композитний індекс для швидкого пошуку пар за кабінетом, датою та часом
CREATE INDEX idx_class_schedule 
ON Пара (Номер_кабінету, Дата, Час_початку);

-- Індекс для швидкого пошуку студентів за групою
CREATE INDEX idx_student_group
ON Студент (Номер_групи);

-- щоб швидко шукати по імені
CREATE FULLTEXT INDEX idx_fulltext_name
ON Людина (ПІБ);
