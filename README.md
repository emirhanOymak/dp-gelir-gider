Projenin son halinde ortak kullanılan DataBase'e ekleme yapılmıştır. Kullanıcı tablosu şu şekilde güncellenmelidir: 
CREATE TABLE Kullanici (
    kullaniciId INT PRIMARY KEY IDENTITY,
    kullaniciAdi NVARCHAR(50) NOT NULL,
    sifre NVARCHAR(255) NOT NULL,
    rol NVARCHAR(20) NOT NULL -- admin, kullanici, izleyici
);
