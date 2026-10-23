import asyncio
from datetime import date, datetime, timedelta
from app.db.session import SessionLocal
from sqlalchemy import text
from app.db.models import User, Book, Location, Stock, Booking
from app.core.security import hash_password
from random import randint

def get_data():
	users = [
		User(
			username="Test User", 
			email="admin@example.com",
			password_hash=hash_password("adminpass"),
			birthday=date(1997, 3, 24)
		),
		User(
			username="yeel", 
			email="yeel@eel.com",
			password_hash=hash_password("somepass"),
			birthday=date(2002, 1, 3)
		)
	]
	books = [
		Book( 
			title="The Hobbit", 
			author="J.R.R. Tolkien", 
			genre="Fantasy", 
			descr="Bilbo Baggins is a hobbit who enjoys a comfortable, unambitious life, rarely travelling further than the pantry of his hobbit-hole in Bag End. But his contentment is disturbed when the wizard Gandalf and a company of thirteen dwarves arrive on his doorstep one day to whisk him away on an unexpected journey ‘there and back again’. They have a plot to raid the treasure hoard of Smaug the Magnificent, a large and very dangerous dragon…" 
		),
		Book( 
			title="The Fellowship of the Ring", 
			author="J.R.R. Tolkien", 
			genre="Fantasy", 
			descr="In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others. But the One Ring was taken from him, and though he sought it throughout Middle-earth, it remained lost to him. After many ages it fell into the hands of Bilbo Baggins, as told in The Hobbit. In a sleepy village in the Shire, young Frodo Baggins finds himself faced with an immense task, as his elderly cousin Bilbo entrusts the Ring to his care. Frodo must leave his home and make a perilous journey across Middle-earth to the Cracks of Doom, there to destroy the Ring and foil the Dark Lord in his evil purpose." 
		),
		Book( 
			title="The Two Towers", 
			author="J.R.R. Tolkien", 
			genre="Fantasy", 
			descr="The Fellowship has fractured. Frodo and Sam travelling covertly towards Mount Doom; Merry and Pippin captured by orcs; Aragorn, Legolas and Gimli on their trail trying to rescue them. And from two separate fronts, the twin forces of Mordor and Isengard ready to launch their final assault to conquer all Middle Earth. A darkness is spreading over the Realm of Men, and a feeble battered resistance, the only obstacle in their way." 
		),
		Book( 
			title="The Return of the King", 
			author="J.R.R. Tolkien", 
			genre="Fantasy", 
			descr="The Companions of the Ring have become involved in separate adventures as the quest continues. Aragorn, revealed as the hidden heir of the ancient Kings of the West, joined with the Riders of Rohan against the forces of Isengard and took part in the desperate victory of the Hornburg. Merry and Pippin, captured by Orcs, escaped into Fangorn Forest and there encountered the Ents. Gandalf returned, miraculously, and defeated the evil wizard, Saruman. Meanwhile, Sam and Frodo progressed toward Mordor to destroy the Ring, accompanied by Sméagol—Gollum, still obsessed by his 'precious'. After a battle with the giant spider, Shelob, Sam left his master for dead; but Frodo is still alive—in the hands of the Orcs. And all the time the armies of the Dark Lord are massing." 
		),
		Book( 
			title="Jurassic Park", 
			author="Michael Crichton", 
			genre="Science fiction", 
			descr="On a remote jungle island, genetic engineers have created a dinosaur game park. An astonishing technique for recovering and cloning dinosaur DNA has been discovered. Now one of mankind's most thrilling fantasies has come true and the first dinosaurs that the Earth has seen in the time of man emerge. But, as always, there is a dark side to the fantasy and after a catastrophe destroys the park's defence systems, the scientists and tourists are left fighting for survival..." 
		),
		Book( 
			title="The Hound of the Baskervilles", 
			author="Arthur Conan Doyle", 
			genre="Mystery", 
			descr="Based on a local legend of a spectral hound that haunted Dartmoor in Devonshire, England, the story is set in the moors at Baskerville Hall and the nearby Grimpen Mire, and the action takes place mostly at night, when the terrifying hound howls for blood. After Sir Charles Baskerville is found dead with his face twisted in stark terror, Holmes is called upon to protect his heir, Sir Henry Baskerville. Narrating the story is Holmes's assistant, Dr. Watson, who is sent to Dartmoor while the busy Holmes remains in London." 
		),
		Book( 
			title="Project Hail Mary", 
			author="Andy Weir", 
			genre="Science fiction", 
			descr="Ryland Grace is the sole survivor on a desperate, last-chance mission - and if he fails, humanity and the earth itself will perish. Except that right now, he doesn't know that. He can't even remember his own name, let alone the nature of his assignment or how to complete it. All he knows is that he's been asleep for a very, very long time. And he's just been awakened to find himself millions of miles from home, with nothing but two corpses for company." 
		),
		Book( 
			title="Dune", 
			author="Frank Herbert", 
			genre="Science fiction", 
			descr="Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the 'spice' melange, a drug capable of extending life and enhancing consciousness. Coveted across the known universe, melange is a prize worth killing for.... When House Atreides is betrayed, the destruction of Paul's family will set the boy on a journey toward a destiny greater than he could ever have imagined." 
		)
	]
	locations = [
		Location(
			country="Russia", 
			city="Moscow",
			street="Aviamotornaya", 
			house="8A", 
			descr="Central branch, university library, open Mon-Sat 9:00-20:00."
		),
		Location(
			country="Russia",
			city="Saint Petersburg",
			street="Ligovsky Prospekt",
			house="142",
			descr="Branch near the shopping district, open daily 10:00-21:00."
		),
		Location(
			country="Germany",
			city="Berlin",
			street="Frankfurter Allee",
			house="63",
			descr="Neighborhood branch with a children's corner, open Tue-Sun 10:00-19:00."
		),
		Location(
			country="United Kingdom",
			city="Manchester",
			street="Oxford Road",
			house="217",
			descr="University-side branch, extended hours during exam season, open Mon-Fri 8:30-20:00."
		),
		Location(
			country="Japan",
			city="Osaka",
			street="Tanimachi 4-chome",
			house="3-12",
			descr="Compact pickup point near the metro, open daily 11:00-22:00."
		)
	]
	stocks = []
	for book in books:
		for location in locations:
			stocks.append(
				Stock(
					book_id=book.book_id, 
					loc_id=location.loc_id, 
					available=randint(0, 5), 
					reserved=0
				)
			)
	now = datetime(2026, 10, 20, 12, 0)
	bookings = [
		# ongoing
		Booking(
			user_id=users[0].user_id, 
			book_id=books[0].book_id, 
			loc_id=locations[0].loc_id,
			time_created=now - timedelta(days=10),
			time_due=now + timedelta(days=4),
			time_closed=None,
			stat="ongoing",
		),
		Booking(
			user_id=users[1].user_id, 
			book_id=books[4].book_id, 
			loc_id=locations[2].loc_id,
			time_created=now - timedelta(days=3),
			time_due=now + timedelta(days=11),
			time_closed=None,
			stat="ongoing",
		),
		# closed
		Booking(
			user_id=users[0].user_id, 
			book_id=books[1].book_id, 
			loc_id=locations[1].loc_id,
			time_created=now - timedelta(days=30),
			time_due=now - timedelta(days=16),
			time_closed=now - timedelta(days=18), # 2 days early
			stat="closed",
		),
		Booking(
			user_id=users[1].user_id, 
			book_id=books[6].book_id, 
			loc_id=locations[4].loc_id,
			time_created=now - timedelta(days=45),
			time_due=now - timedelta(days=31),
			time_closed=now - timedelta(days=28), # 3 days late but ultimately returned
			stat="closed",
		),
		# late
		Booking(
			user_id=users[0].user_id, 
			book_id=books[2].book_id, 
			loc_id=locations[2].loc_id,
			time_created=now - timedelta(days=25),
			time_due=now - timedelta(days=11),
			time_closed=None,
			stat="late",
		),
		# cancelled
		Booking(
			user_id=users[1].user_id, 
			book_id=books[7].book_id, 
			loc_id=locations[3].loc_id,
			time_created=now - timedelta(days=7),
			time_due=now + timedelta(days=7), # due date never mattered
			time_closed=now - timedelta(days=6), # cancelled next day
			stat="cancelled",
		),
		# pending
		Booking(
			user_id=users[0].user_id, 
			book_id=books[3].book_id, 
			loc_id=locations[0].loc_id,
			time_created=now - timedelta(hours=2),
			time_due=now + timedelta(days=14),
			time_closed=None,
			stat="pending",
		),
	]
	return users, books, locations, stocks, bookings

async def seed() -> None:
	async with SessionLocal() as db:
		await db.execute(text(
			"truncate bookings, stock, books, locations, users restart identity cascade"
		))
		await db.commit()

		users, books, locations, stocks, bookings = get_data()
		
		db.add_all(users)
		db.add_all(books)
		db.add_all(locations)
		await db.flush()

		db.add_all(stocks)
		db.add_all(bookings)
		await db.commit()
	print("database ready")

if __name__ == "__main__":
	asyncio.run(seed())
	