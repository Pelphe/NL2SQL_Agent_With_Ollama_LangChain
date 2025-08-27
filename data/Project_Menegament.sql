-- Tabloları Silme
DROP TABLE IF EXISTS addapro;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS CrewMembers;
DROP TABLE IF EXISTS Managers;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;

-- Users Tablosu
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(255),
    UserEmail VARCHAR(255) UNIQUE,
    UserPassword VARCHAR(255),
    UserType VARCHAR(50) -- 'Manager' veya 'CrewMember' gibi
);

-- Managers Tablosu
CREATE TABLE Managers (
    ManagerID INT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- CrewMembers Tablosu
CREATE TABLE CrewMembers (
    CrewMemberID INT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Projects Tablosu
CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY,
    ProjectName VARCHAR(255),
    ProjectDescription VARCHAR(255),
    ProjectStatus VARCHAR(50),
    StartDate DATE,
    EndDate DATE
);

-- Tasks Tablosu
CREATE TABLE Tasks (
    TaskID INT PRIMARY KEY,
    TaskName VARCHAR(50),
    ProjectID INT,
    StartDate DATE,
    EndDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

-- Activities Tablosu
CREATE TABLE Activities (
    ActivityID INT PRIMARY KEY,
    ActivityName VARCHAR(255),
    ActivityType VARCHAR(100),
    ScheduledDate DATE,
    Duration INT,
    ResponsibleManagerID INT,
    FOREIGN KEY (ResponsibleManagerID) REFERENCES Managers(ManagerID)
);

-- Customers Tablosu
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(255),
    CustomerEmail VARCHAR(255),
    PhoneNumber VARCHAR(15)
);

-- adddapro Tablosu
CREATE TABLE addapro (
    EntryID INT PRIMARY KEY,
    ManagerID INT,
    CrewMemberID INT,
    TaskID INT,
    ExperienceNotes TEXT,
    SubmissionDate DATE,
    FOREIGN KEY (ManagerID) REFERENCES Managers(ManagerID),
    FOREIGN KEY (CrewMemberID) REFERENCES CrewMembers(CrewMemberID),
    FOREIGN KEY (TaskID) REFERENCES Tasks(TaskID)
);

-- Users Tablosuna Veri Ekleme
-- Users Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Users (UserID, UserName, UserEmail, UserPassword, UserType) VALUES
(5, 'Ahmet Yılmaz', 'ahmet.yilmaz@example.com', 'ahmetpass', 'Manager'),
(6, 'Fatma Kaya', 'fatma.kaya@example.com', 'fatmapass', 'CrewMember'),
(7, 'Burak Demir', 'burak.demir@example.com', 'burakpass', 'CrewMember');

-- Managers Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Managers (ManagerID, UserID) VALUES
(3, 5);

-- CrewMembers Tablosuna Daha Fazla Veri Ekleme
INSERT INTO CrewMembers (CrewMemberID, UserID) VALUES
(3, 6),
(4, 7);

-- Customers Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Customers (CustomerID, CustomerName, CustomerEmail, PhoneNumber) VALUES
(3, 'Kemal T', 'kemal.t@example.com', '555-9876'),
(4, 'Merve S', 'merve.s@example.com', '555-4321');

-- Projects Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Projects (ProjectID, ProjectName, ProjectDescription, ProjectStatus, StartDate, EndDate) VALUES
(3, 'CRM Sistemi', 'Müşteri ilişkileri yönetim sistemi', 'Tamamlandı', '2023-05-01', '2023-12-15'),
(4, 'Blog Platformu', 'Çok kullanıcılı blog platformu', 'Devam Ediyor', '2024-03-10', '2024-10-30');

-- Tasks Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Tasks (TaskID, TaskName, ProjectID, StartDate, EndDate, Status) VALUES
(4, 'API Entegrasyonu', 3, '2023-06-01', '2023-08-15', 'Tamamlandı'),
(5, 'Test Otomasyonu', 3, '2023-09-01', '2023-11-10', 'Tamamlandı'),
(6, 'Kullanıcı Kayıt Modülü', 4, '2024-03-15', '2024-04-20', 'Devam Ediyor'),
(7, 'Yorum Sistemi', 4, '2024-05-01', '2024-06-15', 'Planlandı');

-- Activities Tablosuna Daha Fazla Veri Ekleme
INSERT INTO Activities (ActivityID, ActivityName, ActivityType, ScheduledDate, Duration, ResponsibleManagerID) VALUES
(3, 'Kod İnceleme', 'Review', '2023-07-10', 45, 3),
(4, 'Demo Sunumu', 'Presentation', '2023-12-10', 30, 1),
(5, 'Sprint Retrospective', 'Meeting', '2024-04-25', 60, 2);

-- addapro (Deneyim Notları) Tablosuna Daha Fazla Veri Ekleme
INSERT INTO addapro (EntryID, ManagerID, CrewMemberID, TaskID, ExperienceNotes, SubmissionDate) VALUES
(3, 3, 3, 4, 'API entegrasyonu sorunsuz tamamlandı.', '2023-08-16'),
(4, 1, 4, 5, 'Test otomasyonu ile hatalar azaldı.', '2023-11-11'),
(5, 2, 2, 6, 'Kullanıcı kayıt modülü için yeni validasyonlar eklendi.', '2024-04-21'),
(6, 3, 6, 7, 'Yorum sistemi için tasarım önerileri hazırlandı.', '2024-06-16');