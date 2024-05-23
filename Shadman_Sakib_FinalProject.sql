create database Restaurants_Reservations;
use Restaurants_Reservations;

create table customers (
    customerId int not null primary key auto_increment,
    customerName varchar(45) not null,
    contactInfo varchar(200)
);

create table reservations (
    reservationId int not null primary key auto_increment,
    customerId int,
    reservationTime datetime not null,
    numberOfGuests int not null,
    specialRequests varchar(200),
    foreign key (customerId) references customers(customerId)
);

create table diningPreferences (
    preferenceId int not null primary key auto_increment,
    customerId int,
    favoriteTable varchar(45),
    dietaryRestrictions varchar(200),
    foreign key (customerId) references customers(customerId)
);

insert into customers(customerName, contactInfo) 
values ('Dia Maya', 'diamaya19@gmail.com'),
	   ('Shadman Sakib', 'shadmansakib780@gmail.com'),
	   ('Asif Haque', '347-939-2967'),
       ('Fahmida Choudhury', 'shiningsun990@gmail.com');


insert into reservations (customerId, reservationTime, numberOfGuests, specialRequests) 
values (1, '2024-07-09 17:00:00', 2, 'Silent part of the restaurant with beautiful scene.'),
	   (2, '2024-10-10 21:00:00', 10, 'Please hide the engagement ring in the cake please!'),
	   (3, '2024-12-23 13:00:00', 20, 'Keep the drinks rolling'),
	   (4, '2025-10-10 15:00:00', 100, 'Additional service staff for the wedding reception will be required.');


insert into diningPreferences (customerId, favoriteTable, dietaryRestrictions) 
values (1, 'Table 1', 'No pork and alcohol on any food.'),
	   (2, 'Table 5', 'No peanut based food'),
	   (3, 'Table 10', 'None'),
	   (4, 'Table 16', 'All the Halal food on the menu');


select * from customers;
select * from reservations;
select * from diningPreferences;


delimiter //
create procedure findReservations(in in_customerId int)
begin
    select * from reservations where customerId = in_customerId;
end //
delimiter ;

delimiter //
create procedure addSpecialRequest(in in_reservationId int, in in_requests varchar(200))
begin
    update reservations set specialRequests = in_requests where reservationId = in_reservationId;
end //
delimiter ;

delimiter //
create procedure addReservation(
    in in_customerName varchar(45), 
    in in_contactInfo varchar(200), 
    in in_reservationTime datetime, 
    in in_numberOfGuests int, 
    in in_specialRequests varchar(200)
)
begin
    declare customerId int;
    
    -- Check if customer already exists
    select customerId into customerId from customers 
    where customerName = in_customerName and contactInfo = in_contactInfo;
    
    if customerId is null then
        insert into customers (customerName, contactInfo) values (in_customerName, in_contactInfo);
        set customerId = LAST_INSERT_ID();
    end if;
    
    insert into reservations (customerId, reservationTime, numberOfGuests, specialRequests) values
    (customerId, in_reservationTime, in_numberOfGuests, in_specialRequests);
end //
delimiter ;
