-- 1. Створення таблиць

-- Створення таблиці Людина
CREATE TABLE Людина (
    Паспорт VARCHAR(20) NOT NULL,
    ПІБ VARCHAR(100) NOT NULL,
    PRIMARY KEY (Паспорт)
);

-- Створення таблиці Студент
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

-- Створення таблиці Член персоналу
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

-- Створення таблиці Член деканату
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

-- Створення таблиці Викладач
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

-- Створення таблиці Член неакадемічного персоналу
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

-- Створення таблиці Директор
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

-- Створення таблиці Група
CREATE TABLE Група (
    Номер INT NOT NULL,  
    Кількість_студентів INT NOT NULL,
    Спеціальність VARCHAR(100) NOT NULL,
    PRIMARY KEY (Номер)
);

-- Створення таблиці Університет
CREATE TABLE Університет (
    ID INT NOT NULL,  
    Назва VARCHAR(70) NOT NULL,
    Адреса VARCHAR(80) NOT NULL,
    Тип VARCHAR(20) NOT NULL,
    Рік_заснування YEAR NOT NULL,
    PRIMARY KEY (ID)
);

-- Створення таблиці Кабінет
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

-- Створення таблиці Захід 
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

-- Створення таблиці Засідання
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

-- Створення таблиці Культурна подія
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

-- Створення таблиці Пара
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

-- Створення таблиці Лекція
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

-- Створення таблиці Практика
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

-- Створення таблиці Екзамен
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

-- Створення таблиці Консультація
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
