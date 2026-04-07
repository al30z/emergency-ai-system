import pandas as pd
import random

random.seed(42)

CRITICAL = [
    "I am trapped under rubble", "Building collapsed, need rescue now",
    "Fire spreading, people inside", "Someone is unconscious and not breathing",
    "Massive flood, children stranded on roof", "Gas leak explosion imminent",
    "Multiple casualties, need ambulance immediately", "Heart attack victim, no pulse",
    "Drowning person spotted in the river", "Injured and bleeding severely",
    "We are trapped in the elevator", "Person fell from 3rd floor unresponsive",
    "Shooting reported, people injured", "House on fire, family trapped",
    "Bridge collapsed, cars in water", "Chemical spill, people exposed",
]

URGENT = [
    "Need medical attention soon", "Elderly person needs insulin now",
    "Baby without food for 12 hours", "Small fire contained but spreading",
    "Road blocked, ambulance can't pass", "Person with broken limb in pain",
    "Out of drinking water, 20 people here", "Diabetic patient needs sugar",
    "Need rescue from flooded ground floor", "Medical supplies running low",
    "Power outage in hospital ward", "Asthma attack, need inhaler",
    "Injured leg, unable to walk", "Shelter damaged, rain entering",
]

MEDIUM = [
    "Need food supplies for our group", "Looking for missing family member",
    "No electricity for 2 days", "Need warm blankets and clothes",
    "Can volunteers come to our area", "Generator needed for the shelter",
    "Request for sanitation supplies", "Pregnant woman needs checkup",
    "Children need vaccines", "Lost contact with relatives",
    "Need transport to evacuation center", "Requesting clean water",
]

LOW = [
    "Any updates on relief operations?", "When will roads reopen?",
    "Is the flood receding?", "Any news on power restoration?",
    "Requesting information about nearby shelters", "What is the weather forecast?",
    "Can someone confirm if school reopens?", "Is the relief camp still active?",
    "General inquiry about aid availability", "Any volunteers needed?",
    "Please share update on flood situation", "Looking for information about donations",
]

def generate_dataset(n=1500):
    data = []
    sources = [
        (CRITICAL, "critical"),
        (URGENT, "urgent"),
        (MEDIUM, "medium"),
        (LOW, "low"),
    ]
    per_class = n // 4
    for messages, label in sources:
        for _ in range(per_class):
            msg = random.choice(messages)
            # slight variation
            if random.random() > 0.5:
                msg = msg.lower()
            data.append({"message": msg, "priority": label})

    random.shuffle(data)
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("backend/data.csv", index=False)
    print(f"Dataset saved: {len(df)} rows")
    print(df["priority"].value_counts())