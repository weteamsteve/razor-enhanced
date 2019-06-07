from Scripts.utilities.items import FindItem
from Scripts.glossary.colors import colors

if Misc.ShardName() == 'UO Evolution':
    petsToCheck = [
        0x002A6E71, # Horse
        0x0015D121, # Zazzy
    ]
else:
    petsToCheck = [
        0x00048E19, # Saphira
        0x00102404, # Your Darkest Nightmare
        0x0001801E, # Metalicana
        0x0009CA1B, # Toothless
    ]

for pet in petsToCheck:
    Timer.Create( 'distanceTimer%s' % pet, 1 )

def HealPets():
    global petsToCheck
    
    bandages = FindItem( 0x0E21, Player.Backpack )
    
    if bandages == None:
        Misc.SendMessage( 'Out of bandages!', colors[ 'red' ] )
        return
    #Misc.SendMessage( 'healing pets' )

    for petSerial in petsToCheck:
        pet = Mobiles.FindBySerial( petSerial )
        if pet == None:
            continue
        #Misc.SendMessage( 'Checking %s\'s health' % pet.Name )
        if Misc.ShardName() == 'UO Evolution':
            maxDistance = 2
        else:
            maxDistance = 1
        if pet.Hits < pet.HitsMax or pet.Poisoned:
            if Player.DistanceTo( pet ) > maxDistance:
                if not Timer.Check( 'distanceTimer%s' % petSerial ):
                    Misc.SendMessage( 'Too far away from %s to apply bandages' % ( pet.Name ), colors[ 'red' ] )
                    Timer.Create( 'distanceTimer%s' % petSerial, 1000 )
                continue

            Items.UseItem( bandages )
            Target.WaitForTarget( 10000, False )
            Target.TargetExecute( pet )
            Player.HeadMessage( colors[ 'cyan' ], 'Applying bandage on %s (currently %i%% health)' % ( pet.Name, ( float( pet.Hits ) / float( pet.HitsMax ) * 100 ) ) )
            
            Misc.Pause( 200 )
            
            bandageDone = False
            while not bandageDone:
                regularText = Journal.GetTextByType( 'Regular' )
                regularText.Reverse()
                for line in regularText[ 0 : len( regularText ) ]:
                    if line == 'You begin applying the bandages.':
                        break
                    if ( line == 'You finish applying the bandages.' or
                            line == 'You heal what little damage your patient had.' or
                            line == 'You did not stay close enough to heal your patient!' or
                            line == 'You apply the bandages, but they barely help.' or
                            line == 'That being is not damaged!' ):
                        bandageDone = True
                        Misc.Pause( 100 )
                        break
                Misc.Pause( 50 )
            return

while not Player.IsGhost:
    HealPets()
    Misc.Pause( 150 )
