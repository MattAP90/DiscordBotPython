import sqlite3

unit_types = """
    CREATE TABLE IF NOT EXISTS "Unit_Types" (
	"id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    PRIMARY KEY("id")	
    );"""

leader_types = """
    CREATE TABLE IF NOT EXISTS "Leader_Types" (
    "id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	PRIMARY KEY("id")	
    );"""

tech_types = """
    CREATE TABLE IF NOT EXISTS "Tech_Types" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	PRIMARY KEY("id")	
    );"""

targets = """
    CREATE TABLE IF NOT EXISTS "Targets" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	PRIMARY KEY("id")	
    );"""

card_types = """
    CREATE TABLE IF NOT EXISTS "Card_Types" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	PRIMARY KEY("id")	
    );"""

planet_traits = """
    CREATE TABLE IF NOT EXISTS "Planet_Traits" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	PRIMARY KEY("id")	
);"""

tech_specialties = """
    CREATE TABLE IF NOT EXISTS "Tech_Specialties" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	PRIMARY KEY("id")	
);"""

factions = """
    CREATE TABLE IF NOT EXISTS "Factions" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"flavor" TEXT NOT NULL,
	"commodoties" TEXT NOT NULL,
	"complexity" TEXT NOT NULL,
	"num_start_techs" TEXT NOT NULL,
	PRIMARY KEY("id")	
);"""

anomalies = """
    CREATE TABLE IF NOT EXISTS "Anomalies" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	PRIMARY KEY("id")	
);"""

systems = """
    CREATE TABLE IF NOT EXISTS "Systems" (
	"id" INTEGER NOT NULL UNIQUE,
	"anomaly" INTEGER,
	"alpha" INTEGER,
	"beta" INTEGER,
	"gamma" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("anomaly") REFERENCES "Anomalies"("id")
);"""

home_systems = """
    CREATE TABLE IF NOT EXISTS "Home_Systems" (
	"id" INTEGER NOT NULL UNIQUE,
	"faction_id" INTEGER,
	"anomaly" INTEGER,
	"delta" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id"),
	FOREIGN KEY ("anomaly") REFERENCES "Anomalies"("id")
);"""

techs = """
    CREATE TABLE IF NOT EXISTS "Techs" (
	"id" INTEGER NOT NULL,
	"type" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"text" TEXT NOT NULL,
	"red_prereq" INTEGER NOT NULL,
	"blue_prereq" INTEGER NOT NULL,
	"yellow_prereq" INTEGER NOT NULL,
	"green_prereq" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("type") REFERENCES "Tech_Types"("id")
);"""

faction_techs = """
    CREATE TABLE IF NOT EXISTS "Faction_Techs" (
	"id" INTEGER NOT NULL,
	"faction_id" INTEGER NOT NULL,
	"type" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"text" TEXT NOT NULL,
	"red_prereq" INTEGER NOT NULL,
	"blue_prereq" INTEGER NOT NULL,
	"yellow_prereq" INTEGER NOT NULL,
	"green_prereq" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id"),
	FOREIGN KEY ("type") REFERENCES "Tech_Types"("id")
);"""

planets = """
    CREATE TABLE IF NOT EXISTS "Planets" (
	"id" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"flavor" TEXT NOT NULL,
	"resouces" INTEGER NOT NULL,
	"influence" INTEGER NOT NULL,
	"trait" INTEGER NOT NULL,
	"tech_specialty" INTEGER NOT NULL,
	"system_id" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("trait") REFERENCES "Planet_Traits"("id"),
	FOREIGN KEY ("tech_specialty") REFERENCES "Tech_Specialties"("id"),
	FOREIGN KEY ("system_id") REFERENCES "Systems"("id")
);"""

starting_units = """
    CREATE TABLE IF NOT EXISTS "Starting_Units" (
	"faction_id" INTEGER NOT NULL,
	"flagship" TEXT NOT NULL,
	"war_sun" TEXT NOT NULL,
	"dreadnought" TEXT NOT NULL,
	"carrier" TEXT NOT NULL,
	"cruiser" TEXT NOT NULL,
	"destroyer" TEXT NOT NULL,
	"fighter" TEXT NOT NULL,
	"pds" TEXT NOT NULL,
	"infantry" TEXT NOT NULL,
	"space_dock" TEXT NOT NULL,
	"mech" TEXT NOT NULL,
	PRIMARY KEY("faction_id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id")
);"""

cards = """
    CREATE TABLE IF NOT EXISTS "Cards" (
	"id" INTEGER NOT NULL,
	"type" INTEGER NOT NULL,
	"target" INTEGER NOT NULL,
	"title" TEXT NOT NULL,
	"text" TEXT NOT NULL,
	"flavor" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("type") REFERENCES "Card_Types"("id"),
	FOREIGN KEY ("target") REFERENCES "TARGETS"("id")
);"""

units = """
    CREATE TABLE IF NOT EXISTS "Units" (
	"id" INTEGER NOT NULL,
	"type" INTEGER NOT NULL,
	"name" TEXT NOT NULL,
	"cost" TEXT NOT NULL,
	"produced" TEXT NOT NULL,
	"combat" TEXT NOT NULL,
	"rolls" TEXT NOT NULL,
	"move" TEXT NOT NULL,
	"capacity" TEXT NOT NULL,
	"abilities" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("type") REFERENCES "Unit_Types"("id")
);"""

starting_techs = """
    CREATE TABLE IF NOT EXISTS "Starting_Techs" (
	"id" INTEGER,
	"faction_id" INTEGER NOT NULL,
	"tech_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id"),
	FOREIGN KEY ("tech_id") REFERENCES "Techs"("id")
);"""

leaders = """
    CREATE TABLE IF NOT EXISTS "Leaders" (
	"id" INTEGER NOT NULL,
	"faction_id" INTEGER NOT NULL,
	"leader_type" INTEGER NOT NULL,
	"leader_name" TEXT NOT NULL,
	"leader_unlock" TEXT NOT NULL,
	"leader_ability" TEXT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("leader_type") REFERENCES "Leader_Types"("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id")
);"""

legendary_planets = """
    CREATE TABLE IF NOT EXISTS "Legendary_Planets" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"flavor" TEXT,
	"resources" INTEGER,
	"influence" INTEGER,
	"trait" INTEGER,
	"ability" TEXT,
	"unlock" TEXT,
	"system_id" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("trait") REFERENCES "Planet_Traits"("id"),
	FOREIGN KEY ("system_id") REFERENCES "Systems"("id")
);"""

home_planets = """
    CREATE TABLE IF NOT EXISTS "Home_Planets" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"flavor" TEXT,
	"resources" INTEGER,
	"influence" INTEGER,
	"system_id" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("system_id") REFERENCES "Home_Systems"("id")
);"""

faction_units = """
    CREATE TABLE IF NOT EXISTS "Faction_Units" (
	"id" INTEGER NOT NULL UNIQUE,
	"faction_id" INTEGER,
	"name" TEXT,
	"cost" TEXT,
	"produced" TEXT,
	"combat" TEXT,
	"rolls" TEXT,
	"move" TEXT,
	"capacity" TEXT,
	"abilities" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id")
);"""

faction_abilities = """
    CREATE TABLE IF NOT EXISTS "Faction_Abilities" (
	"id" INTEGER NOT NULL UNIQUE,
	"faction_id" INTEGER,
	"name" TEXT,
	"text" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("faction_id") REFERENCES "Factions"("id")
);"""

rules = """
    CREATE TABLE IF NOT EXISTS "Rules" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"text" TEXT,
	PRIMARY KEY("id")	
);"""

sub_section = """
    CREATE TABLE IF NOT EXISTS "Sub_Section" (
	"id" INTEGER NOT NULL UNIQUE,
	"rule_id" INTEGER,
	"section_num" INTEGER,
	"text" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("rule_id") REFERENCES "Rules"("id")
);"""

rules_index = """
    CREATE TABLE IF NOT EXISTS "Rules_Index" (
	"id" INTEGER NOT NULL UNIQUE,
	"keyword" TEXT,
	"rules_section" TEXT,
	PRIMARY KEY("id")	
);"""

strategy_cards = """
    CREATE TABLE IF NOT EXISTS "Strategy_Cards" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"initiative" INTEGER,
	"primary" TEXT,
	"secondary" TEXT,
	PRIMARY KEY("id")	
);"""

connection = sqlite3.connect('TI4.db')
cursor = connection.cursor()
cursor.execute(unit_types)
cursor.execute(leader_types)
cursor.execute(tech_types)
cursor.execute(targets)
cursor.execute(card_types)
cursor.execute(planet_traits)
cursor.execute(tech_specialties)
cursor.execute(factions)
cursor.execute(anomalies)
cursor.execute(systems)
cursor.execute(home_systems)
cursor.execute(techs)
cursor.execute(faction_techs)
cursor.execute(planets)
cursor.execute(starting_units)
cursor.execute(cards)
cursor.execute(units)
cursor.execute(starting_techs)
cursor.execute(leaders)
cursor.execute(legendary_planets)
cursor.execute(home_planets)
cursor.execute(faction_units)
cursor.execute(faction_abilities)
cursor.execute(rules)
cursor.execute(sub_section)
cursor.execute(rules_index)
cursor.execute(strategy_cards)

connection.close()
