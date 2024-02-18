#https://gemini.google.com/app/62f319aef93f2156

phase_order = ['Beginning Phase','Pre-combat Main Phase','Combat Phase','Post-combat Main Phase','Ending Phase']
beginning_phase_order = ['Untap Step','Upkeep Step','Draw Step']
main_phase_order = []
combat_phase_order = ['Beginning of Combat Step, Declare Attackers Step, Declare Blockers Step, Calculate Damage Step, End of Combat Step']
ending_phase_order = ['End Step', 'Cleanup Step']

current_phase = 'Beginning Phase'
current_phase = 'Pre-combat Main Phase'
index = phase_order.index(current_phase)
index += 1

print(index)

