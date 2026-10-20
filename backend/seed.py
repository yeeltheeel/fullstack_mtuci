import asyncio
from sqlalchemy import text
from app.db.engine import engine

async def seed() -> None:
	async with engine.begin() as conn:
		await conn.execute(text("""
			create table if not exists users(
				user_id serial primary key,
				username varchar(100)
			)
		"""))
		await conn.execute(
			text("delete from users")
		)
		await conn.execute(
			text(
				"insert into users(username) values (:n1), (:n2)"
			), 
			{
				"n1": "user1", 
				"n2": "user2"
			}
		)
	print("database ready")

if __name__ == "__main__":
	asyncio.run(seed())