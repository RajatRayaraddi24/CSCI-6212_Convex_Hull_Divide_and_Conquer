import matplotlib.pyplot as plt

#Sum(Theoretical): 68347284.4515057
#Sum(Experimental): 15485302125
#Scaling Factor: 226.56792072

ns = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]

times = [
    819012584,
    1628177542,
    2973560250,
    3370169666,
    4515335167,
    6017685458,
    6865776625,
    6838229875
]

theoretical = [
    802639537.854234,
    1701926506.34847,
    2637692443.59588,
    3597147873.97694,
    4574218650.52541,
    5565327179.11176,
    6568109505.36963,
    7580885470.5139
]

plt.figure(figsize=(12, 8))
plt.plot(ns, times, marker='o', label='Experimental Time', color = 'blue')
plt.plot(ns, theoretical, marker='*', label='Theoretical Result', color = 'red')
plt.title('Experimental vs Theoretical Time')
plt.xlabel('Number of Points (n)')
plt.ylabel('Time (ns)')
plt.legend()
plt.grid(True)
plt.show()