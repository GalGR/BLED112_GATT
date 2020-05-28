% C:\Work\Python\BLED112_GATT\log
a = csvread('C:\Work\Python\BLED112_GATT\log\encoder_log.csv');
figure(1)
hold off
% x1=100;
x1=length(a);
% x2= 9*x1;
% plot(x,'o')

% adjust the X axis index of the 2 mSec sample to the overSample indices 
% xa = 9*a(:,1)-8;
% xa = 10*a(:,1)-9;

% always start the indices from 1

plot(a(1:x1,2),'-or')
hold on
plot(a(1:x1,3),'-og')

% plot(a(1:x1),a(1:x1,2),'-or')
% return

% hold on

