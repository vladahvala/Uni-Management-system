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
    Посада VARCHAR(50) NOT NULL,
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


-- Зв'язки сутності Пара

