# envirozen
Environmental monitoring and control of a room

### Temperature Control for Server Room

This project was initiated using an Arduino to regulate the server room's temperature. It employs two 1.5Kw fans to introduce external ambient air into the room whenever the temperature falls below the (MAX3) threshold. This process creates a positive pressure inside the room, expelling warmer air through specialized vents. The primary objective is to conserve energy on cooler days by leveraging the ambient air, reducing the reliance on air conditioning units when they're not necessary.

As of October 2023 this will developed into Python for deployment onto a more powerful Rasberry Pi

**Started**: October 2022  
**Reason**: Before the cost of electricity started to rise  
**Author**: Nic Kilby

**Component List**

[Raspberry Pi 4 or better][1] for the central controller

[Enviro Indoor (Pico W Aboard) – Enviro Indoor + Accessory Kit][2] x number of areas to monitor

[Fan 1.5Kw ][3] x 2

[TUNE-S-600x600-M1][4] Mechanical damper with M1 Actuator


![Flow of Logic](docs/images/freeair.webp)

[1]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[2]: https://shop.pimoroni.com/products/enviro-indoor?variant=40055644717139
[3]: https://www.plugandcool.co.uk/product/1-5-grain-store-fan/
[4]: https://www.puravent.co.uk/tune-s-600x600-m1.html