import random
import math
import numpy as np
from typing import Literal, Tuple, Union
from colorama import Fore, Back, Style, init

class BasicSecurity:
    style_list=['AlphaNumeric', 'Alpha', 'Numeric']
    fruits = np.array([
        ["apple", "apricot", "avocado", "banana", "blackberry", "blackcurrant", "blueberry", 
        "cantaloupe", "cherry", "clementine", "coconut", "cranberry", "currant", "date", 
        "dragonfruit", "elderberry", "feijoa", "fig", "grape", "grapefruit", "guava", "honeydew", 
        "jackfruit", "jambolan", "jasmine", "kiwi", "kumquat", "lemon", "lime", "lychee", 
        "mandarin", "mango", "mulberry", "nectarine", "orange", "papaya", "passionfruit", "peach", 
        "pear", "persimmon", "pineapple", "plum", "pomegranate", "prickly pear", "raspberry", 
        "red currant", "starfruit", "strawberry", "tangerine", "watermelon", "acai", "allspice", 
        "almond", "amaranth", "anise", "apple pear", "apricot", "arrowroot", "artichoke", 
        "asparagus", "aubergine", "balsam apple", "banana apple", "bitter melon", "black salsify", 
        "bok choy", "broad bean", "brussels sprout", "butternut squash", "cabbage", "carrot", 
        "cauliflower", "celeriac", "chard", "chayote", "chicory", "chili pepper", "chinese cabbage", 
        "chives", "coriander", "cress", "cucumber", "dandelion greens", "dandelion root", 
        "daikon radish", "endive", "fennel", "fennel bulb", "fenugreek", "garlic", "ginger", 
        "horseradish", "jalapeno", "kale", "kohlrabi", "leek", "lettuce", "mango", "mustard greens", 
        "okra", "olive", "onion", "oregano", "paprika", "parsnip", "pea", "potato", "pumpkin", 
        "radish", "rhubarb", "rosemary", "sage", "scallion", "shallot", "spinach", "squash", 
        "sweet potato", "tarragon", "thyme", "tomato", "turnip", "yam", "zucchini", "acorn squash", 
        "arugula", "aubergine", "avocado pear", "bamboo shoot", "basil", "beetroot", "bitter gourd", 
        "bok choy", "broccoli", "brussels sprouts", "butternut squash", "cabbage", "carrot", 
        "cauliflower", "celeriac", "chayote", "chili pepper", "chinese cabbage", "chives", "coriander", 
        "cress", "cucumber", "dandelion greens", "daikon radish", "endive", "fennel", "fenugreek", 
        "garlic", "ginger", "horseradish", "jalapeno", "kale", "kohlrabi", "leek", "lettuce", 
        "mango", "mustard greens", "okra", "olive", "onion", "oregano", "paprika", "parsnip", 
        "pea", "potato", "pumpkin", "radish", "rhubarb", "rosemary", "sage", "scallion", "shallot", 
        "spinach", "squash", "sweet potato", "tarragon", "thyme", "tomato", "turnip", "yam", "zucchini", 
        "amaranth", "apple", "apricot", "avocado", "banana", "blackberry", "blackcurrant", "blueberry", 
        "cantaloupe", "cherry", "clementine", "coconut", "cranberry", "currant", "date", "dragonfruit", 
        "elderberry", "feijoa", "fig", "grape", "grapefruit", "guava", "honeydew", "jackfruit", 
        "jambolan", "jasmine", "kiwi", "kumquat", "lemon", "lime", "lychee", "mandarin", "mango", 
        "mulberry", "nectarine", "orange", "papaya", "passionfruit", "peach", "pear", "persimmon", 
        "pineapple", "plum", "pomegranate", "prickly pear", "raspberry", "red currant", "starfruit", 
        "strawberry", "tangerine", "watermelon", "zinfandel grape", "berries", "citrus", "melons", "tropical fruits",
        "ackee", "acorn squash", "african horned cucumber", "almond", "ambarella", "american persimmon", 
        "applesauce fruit", "apples", "australian finger lime", "autumn olive", "banana passionfruit", 
        "baobab fruit", "barbadine", "barberry", "bayberry", "ber", "bilberry", "bitter orange", "black cherry", 
        "black figs", "black persimmon", "black sapote", "blue java banana", "bocadillo", "bok choi", "bolivian peach", 
        "bottle gourd", "breadfruit", "brazil nut", "buddha's hand", "buffalo gourd", "burdock", "cabelluda", 
        "calamansi", "candied citron", "canistel", "capulin cherry", "cardamom", "carob", "chayote squash", "che", 
        "cherry plum", "cherry tomato", "chilean guava", "clementine mandarin", "cloudberry", "coco plum", 
        "cocoanut", "colocasia", "common fig", "cornelian cherry", "cranapple", "creeping raspberry", "cucumber melon", 
        "custard apple", "damson plum", "dawn redwood", "dewberry", "durian", "eastern redbud", "elderflower", 
        "empress plum", "feather cactus", "fennel bulb", "finger lime", "fuzzy kiwi", "gean cherry", "gala apple", 
        "galapagos tomato", "gambooge", "gaya fruit", "goya", "grape cherry", "grape hyacinth", "grapefruit", 
        "grewia", "guarana", "gull leaf", "hackberry", "hardy kiwi", "hops", "huckleberry", "ice cream bean", 
        "indian fig", "jelly palm", "jew's mallow", "jicama", "juneberry", "kiwano", "korlan", "kumquat", 
        "laburnum", "lansones", "lemon aspen", "lemonade fruit", "longan", "loquat", "lucuma", "lychee", 
        "mandala fruit", "mangaba", "mangosteen", "maui tangelo", "melinjo", "melon pear", "mesquite", "mimosa", 
        "mirabelle", "monstera", "mulberry", "muscadine", "nance", "naranjilla", "nashi pear", "natal plum", 
        "olive oil fruit", "opuntia", "orange", "otahuti", "passionfruit", "peach apple", "peanut", "pear",
        "pecan", "peppercorn", "persimmon", "pineapple guava", "pineberry", "plumcot", "plum", "pluerry", 
        "pomegranate", "popcorn plant", "prickly pear", "pulasan", "quince", "raisin", "rambutan", "red banana", 
        "red pear", "rosemaling", "ruby grape", "sacha inchi", "salak", "satsuma", "soursop", "sugar apple", 
        "sweet lime", "tamarillo", "tamarind", "tangor", "tangerine", "thai lychee", "thimbleberry", 
        "thornless blackberry", "thunder fruit", "tree tomato", "true mango", "tulip tree", "water apple", 
        "water chestnut", "wax jambu", "wild apple", "wild cherry", "wild plum", "yali pear", "yellow mombin", 
        "yellow watermelon", "zante currant", "zapote", "ziziphus"]
    ])
    flowers = np.array([
        ["acacia", "african daisy", "alstroemeria", "amaryllis", "anemone", "angelonia", "aster", 
        "azalea", "begonia", "bluebell", "bougainvillea", "bromeliad", "buttercup", "cala lily", 
        "camellia", "canna", "carnation", "cherry blossom", "chrysanthemum", "clover", "crocus", 
        "daffodil", "dahlia", "daisy", "freesia", "gardenia", "geranium", "ginger lily", "gladiolus", 
        "gloxinia", "hibiscus", "hollyhock", "hydrangea", "impatiens", "iris", "jasmine", "jewel orchid", 
        "lavender", "lily", "lupine", "magnolia", "marigold", "orchid", "pansy", "peony", "petunia", 
        "phlox", "plumeria", "primrose", "roses", "snapdragon", "sunflower", "sweet pea", "tulip", 
        "verbena", "violet", "wisteria", "zinnia", "acacia", "allium", "aster", "bellflower", "bird of paradise", 
        "bouvardia", "butterfly bush", "california poppy", "campanula", "cineraria", "clematis", "columbine", 
        "coneflower", "coreopsis", "coral vine", "cow parsnip", "cyclamen", "daffodil", "dahlia", 
        "delphinium", "dogwood", "fuchsia", "gerbera", "hebe", "hoya", "impatiens", "indigo", "jacaranda", 
        "jasmine", "lilac", "lupine", "maranta", "mimosa", "monarda", "orange blossom", "petunia", 
        "plumeria", "poinsettia", "quince", "rhododendron", "rosemary", "saffron", "sunflower", 
        "sweet william", "tiger lily", "tulip", "violet", "water lily", "yellow bells", "zinnia", 
        "azalea", "butterfly bush", "calendula", "canna lily", "celosia", "cherry blossom", "cineraria", 
        "corydalis", "cress", "daffodil", "daisy", "dandelion", "echinacea", "elephant ear", "fuchsia", 
        "geranium", "globe thistle", "gloxinia", "helenium", "hibiscus", "hollyhock", "honeysuckle", 
        "jasmine", "lupine", "marigold", "mimosa", "musk rose", "orchid", "pansy", "peony", "petunia", 
        "plumeria", "poppy", "ranunculus", "rose", "saffron", "snowdrop", "squill", "sunflower", 
        "tulip", "violet", "wisteria", "wild ginger", "zinnia"]
    ])

    animals = np.array([
        ["aardvark", "alpaca", "ant", "anteater", "armadillo", "asian elephant", "baboon", "badger", 
        "bald eagle", "bandicoot", "bat", "bear", "beaver", "bee", "bison", "booby", "buffalo", 
        "bull", "bunny", "butterfly", "camel", "canary", "capybara", "caribou", "cat", "caterpillar", 
        "cattle", "cheetah", "chicken", "chimpanzee", "chinchilla", "chipmunk", "clam", "cobra", 
        "cockroach", "cod", "cow", "coyote", "crab", "crane", "crow", "crocodile", "crow", "deer", 
        "dingo", "dog", "dolphin", "donkey", "dragonfly", "duck", "eagle", "elephant", "elk", 
        "emu", "falcon", "ferret", "fish", "flamingo", "fox", "frog", "gazelle", "giraffe", "goat", 
        "goose", "gorilla", "guinea pig", "hawk", "hedgehog", "heron", "hippopotamus", "horse", 
        "housefly", "human", "hyena", "ibex", "iguana", "impala", "jaguar", "jellyfish", "kangaroo", 
        "koala", "komodo dragon", "kookaburra", "lamb", "leopard", "lion", "lizard", "llama", 
        "lobster", "locust", "lynx", "manatee", "mandrill", "mole", "mongoose", "monkey", "moose", 
        "mouse", "octopus", "orangutan", "ostrich", "otter", "owl", "ox", "panda", "parrot", 
        "partridge", "peacock", "pelican", "penguin", "pig", "pigeon", "polar bear", "porcupine", 
        "rabbit", "raccoon", "rat", "raven", "reindeer", "rhinoceros", "rooster", "salamander", 
        "scorpion", "seahorse", "seal", "shark", "sheep", "shrimp", "skunk", "slug", "snake", 
        "spider", "squid", "squirrel", "starfish", "stoat", "swallow", "swan", "tapir", 
        "tarantula", "toad", "tortoise", "toucan", "tuna", "turkey", "turtle", "vulture", 
        "wallaby", "walrus", "warthog", "wasp", "weasel", "whale", "wild boar", "wolf", "wombat", "zebra"]
    ])
    movies = np.array([
        ["avatar", "avengers: endgame", "the dark knight", "inception", "fight club", "the godfather", 
        "pulp fiction", "the shawshank redemption", "the matrix", "forrest gump", "the lion king", 
        "star wars: a new hope", "the empire strikes back", "the return of the king", "joker", "gladiator", 
        "the godfather: part ii", "goodfellas", "schindler's list", "the silence of the lambs", "citizen kane", 
        "the dark knight rises", "star wars: the force awakens", "star wars: the last jedi", "the avengers", 
        "mad max: fury road", "interstellar", "titanic", "the princess bride", "the departed", "the social network", 
        "the wolf of wall street", "whiplash", "the big lebowski", "american beauty", "reservoir dogs", 
        "the usual suspects", "the shining", "fight club", "jaws", "casablanca", "the godfather: part iii", 
        "die hard", "jurassic park", "back to the future", "the breakfast club", "e.t. the extra-terrestrial", 
        "goodfellas", "the lion king", "scream", "harry potter and the sorcerer's stone", "harry potter and the chamber of secrets", 
        "harry potter and the prisoner of azkaban", "the matrix revolutions", "dunkirk", "moonlight", "la la land", 
        "blade runner", "the princess bride", "the grand budapest hotel", "eternal sunshine of the spotless mind", 
        "the curious case of benjamin button", "the dark knight", "once upon a time in hollywood", "fargo", "goodfellas", 
        "eternal sunshine of the spotless mind", "the pursuit of happiness", "the big short", "memento", "inception", 
        "the revenant", "her", "gladiator", "a clockwork orange", "the great gatsby", "inglourious basterds", 
        "the shape of water", "12 angry men", "american history x", "whiplash", "pulp fiction", "the princess bride", 
        "the notebook", "the sound of music", "the wizard of oz", "the martian", "crazy rich asians", "kingsman: the secret service", 
        "the hunger games", "scarface", "the shining", "the godfather", "batman begins", "captain america: the first avenger", 
        "x-men", "iron man", "the incredible hulk", "thor", "spider-man", "black panther", "guardians of the galaxy", 
        "wonder woman", "man of steel", "justice league", "avengers: infinity war", "avengers: age of ultron", "the avengers"]
    ])
    celebrities = np.array([
        ["adam sandler", "angelina jolie", "brad pitt", "beyoncé", "bill gates", "blake lively", "bradley cooper", 
        "britney spears", "charlize theron", "chris hemsworth", "chris pratt", "chris rock", "claire danes", 
        "cameron diaz", "cate blanchett", "channing tatum", "colin farrell", "dwayne johnson", "emma stone", 
        "ellen degeneres", "elizabeth taylor", "george clooney", "gisele bündchen", "helen mirren", "hugh jackman", 
        "jacob elordi", "jared leto", "jennifer aniston", "jennifer lopez", "julia roberts", "kate hudson", 
        "katy perry", "kevin hart", "leonardo dicaprio", "lupita nyong'o", "madonna", "matthew mcconaughey", 
        "megan fox", "meryl streep", "michael jackson", "miley cyrus", "morgan freeman", "nicole kidman", 
        "orlando bloom", "oscar isaac", "reese witherspoon", "robert downey jr.", "ryan gosling", "ryan reynolds", 
        "sandra bullock", "scarlett johansson", "selena gomez", "serena williams", "shakira", "sophia vergara", 
        "tom cruise", "tom hanks", "taylor swift", "the rock", "will smith", "will ferrell", "zoe saldana", 
        "zac efron", "al pacino", "angela bassett", "ben affleck", "beyoncé", "brad pitt", "cameron diaz", 
        "carrie underwood", "charlize theron", "chris evans", "chris hemsworth", "chris pratt", "claire danes", 
        "colin farrell", "dwayne johnson", "ellen degeneres", "emily blunt", "emma stone", "george clooney", 
        "gisele bündchen", "hugh jackman", "jake gyllenhaal", "jared leto", "jennifer aniston", "jennifer lopez", 
        "johnny depp", "kate winslet", "kendall jenner", "kerry washington", "kim kardashian", "kristen bell", 
        "leonardo dicaprio", "lucy liu", "matthew mcconaughey", "miley cyrus", "naomi watts", "olivia wilde", 
        "oprah winfrey", "penélope cruz", "reese witherspoon", "robert downey jr.", "ryan gosling", "ryan reynolds", 
        "sandra bullock", "scarlett johansson", "selena gomez", "shakira", "taylor swift", "tom hanks", "tom cruise"]
    ])
    anime_characters = np.array([
        ["naruto uzumaki", "sasuke uchiha", "sakura haruno", "kakashi hatake", "iruka umino", 
        "shikamaru nara", "temari", "neji hyuga", "hinata hyuga", "rock lee", 
        "matthew crawley", "sai", "jiraiya", "pain", "konan", "tobi", "minato namikaze", 
        "itachi uchiha", "kaguya otsutsuki", "obito uchiha", "madara uchiha", "kaguya otsutsuki", 
        "monkey d. luffy", "roronoa zoro", "nami", "usopp", "sanji", "tony tony chopper", 
        "nico robin", "franky", "brook", "jimbei", "portgas d. ace", "trafalgar d. water law", 
        "shanks", "bartholomew kuma", "sabo", "eustass kid", "hawkins", "fujitora", "doflamingo", 
        "kaido", "big mom", "blackbeard", "buggy the clown", "kizaru", "akainu", "zoro", "big mom", 
        "luffy", "reigen arataka", "mob", "shigeo kageyama", "teruki suwen", "tomekichi", "akihiro",
        "koyomi araragi", "hitagi senjougahara", "meme oshino", "swordfish", "aruka", "saber", 
        "rin tohsaka", "shiro emiya", "sakura matou", "kurumi tokisaki", "miku nakano", "nino nakano",
        "ichiha sasuke", "tetsuya kuroko", "ryouta kise", "taiga aisaka", "yuki nagato", "haruhi suzumiya",
        "kyo sohma", "shigure sohma", "yuki sohma", "shun", "mitsuki", "karen araragi", "hyouka", "ecchi",
        "takamatsu", "kemono", "tomoya okazaki", "kotomi ichinose", "nagisa furukawa", "yukino yukinoshita", 
        "shiro", "iruka umino", "hikigaya hachiman", "bunny", "yui", "mikasa ackerman", "eren jaeger",
        "armin arlert", "levi ackerman", "jean kirstein", "sasha blause", "connie springer", "annie leonhart",
        "bertholdt", "reiner braun", "hange zoe", "erwin smith", "mikasa ackerman", "rikka takanashi", 
        "shiro", "danganronpa", "charlotte", "touka kirishima", "kaneki ken", "toka kirishima", "maki", 
        "goku", "vegeta", "piccolo", "krillin", "bulma", "trunks", "majin buu", "frieza", "cell", "android 18",
        "broly", "kail", "tien", "yamcha", "chi-chi", "pan", "goku black", "zamasu", "jiren", "hit",
        "nozel", "yuno", "finral", "asta", "yuji itadori", "megumi fushiguro", "nobara kugisaki", "satoru gojo", 
        "yuta okkotsu", "mahito", "sukuna", "ryomen sukuna", "kamiya", "toji fushiguro", "yuji itadori", 
        "nanami kento", "shoko ieiri", "kento nanami", "maki zenin", "todos", "ryuji sakamoto", "asuka langley", 
        "shinji ikari", "rei ayanami", "gendo ikari", "misato katsuragi", "asuka langley", "kaoru nagisa", 
        "armageddon", "nina", "shinji", "nagisa shiota", "koro-sensei", "tadaomi kyogoku", "ozaki", "hanekawa",
        "hestia", "bell cranel", "aisu", "arlecchino", "meliodas", "escanor", "merlin", "ban", "king", "diane",
        "julius novachrono", "yami sukihira", "sally", "hasoka", "zoro", "chopper", "tetsuo", "goku", "allen walker",
        "kurapika", "gon freecss", "killua zoldyck", "leorio", "huge", "illumi", "knuckle", "knov", "silva",
        "kyogre", "ash ketchum", "misty", "brock", "pikachu", "serena", "chloe", "iris", "dawn", "may",
        "bulbasaur", "charizard", "squirtle", "sheldon", "team rocket", "rattata", "eevee", "snorlax",
        "electrode", "magnemite", "jigglypuff", "rapidash", "taillow", "zubat", "mawile", "lucario", "gengar",
        "machamp", "sableye", "combusken", "swampert", "seaking", "shiny", "raichu", "bulbasaur", "bruno", "claudia",
        "zeref", "akuma", "chika fujiwara", "shiro", "miyuki shirogane", "kaguya shinomiya", "kyouya mitsuboshi",
        "ishigami yu", "izumi saionji", "suzuya", "rika", "alice", "reigen arataka", "kageyama", "yuri katsuki",
        "victor nikiforov", "yuuri katsuki", "yuri", "nonon jakuzure", "makunouchi ippo", "takumi", "renji",
        "shinra kusakabe", "shinra", "maki"]  
    ])
    
    gaming_ids = np.array([
        ["shadowstrike", "nightshade", "blazeclaw", "phantomx", "stormrider", "darkninja", "frostbite", 
        "vortexviper", "cyberwolf", "soulcrusher", "ghostblade", "ironfist", "silentshadow", "flamefang", 
        "deathbringer", "shadowfury", "skybreaker", "stormhawk", "viperstrike", "dragonflare", 
        "nightwhisper", "thunderclash", "voidslinger", "reaperx", "blazeheart", "stealthstrike", 
        "warhammer", "ironclad", "moonshadow", "nightprowler", "stormrage", "viperclaw", "redhawk", 
        "cyberstorm", "shadowfire", "phantomstrike", "crimsonrage", "silverblade", "thunderstrike", 
        "deadshot", "ravenspirit", "blackthorn", "icephoenix", "darkfire", "deathknight", "skyhunter", 
        "xenonblade", "shadowhunter", "stealthwarrior", "bloodreaper", "flamecaster", "blackstorm", 
        "frostwolf", "phantomreaper", "midnightrider", "stormbringer", "darkangel", "moonblade", 
        "blazemaster", "steelfang", "ragingbull", "ironviper", "thunderwolf", "nightshade", "blazeheart", 
        "shadowforce", "galehunter", "firestrike", "wildfire", "frostbite", "dragonslayer", "nightmarex", 
        "reapersoul", "cyberclaw", "soulfire", "thunderfury", "flamethrower", "earthshaker", "soulstorm", 
        "ironblade", "shadowmancer", "blitzkrieg", "snowstorm", "flamefury", "eclipseblade", "bloodfang", 
        "stormrider", "phantomghost", "nightfury", "clashbringer", "raijun", "blademaster", "blackdragon", 
        "spartanx", "deathflare", "viperx", "stormbringer", "maverickx", "silverwolf", "goldenphoenix", 
        "infernohawk", "skyshatter", "venomstrike", "stormdragon", "crimsonblaze", "ghostrider", "soulstrike", 
        "cybershadow", "moonflare", "shadowviper", "mysticdragon", "icefang", "flameburst", "swiftblade", 
        "lightningstorm", "ironwolf", "shadowfury", "deathstorm", "moonfire", "dragonsoul", "soulshatter", 
        "neonflame", "nightstorm", "vortexfury", "bloodhunter", "bloodraven", "hellstorm", "blazeclaw", 
        "darkreaper", "doomblade", "stealthstorm", "darkphoenix", "flamestorm", "silentreaper", 
        "viperfang", "phoenixsoul", "shadowflare", "stormwraith", "reapershadow", "thunderclaw", "blackfire", 
        "frostshade", "warlockx", "thunderfury", "voidreaper", "deathblaze", "stormstrike", "bloodvenom", 
        "shadowraider", "frostphoenix", "nightblade", "blazingshadow", "darkblade", "starlightstorm", 
        "frostfang", "ironstorm", "skyshadow", "bloodthirst", "warstorm", "iceclaw", "flamereaper", 
        "shadowmist", "lightbringer", "darkphoenix", "dreadstorm", "mysticshadow", "blazeveil", "nightshade", 
        "whiteshadow", "thunderstorm", "ironfury", "flameprince", "silentblade", "neonshadow", "vortexflame", 
        "goldenglow", "darkwhisper", "flamethunder", "vortexwarrior", "nightprince", "darkangelx", 
        "firestorm", "roguemaster", "ghostflame", "neonreaper", "stormrage", "bloodstorm", "stormblade", 
        "icefire", "darkstorm", "tigerclaw", "deathstrike", "frostclaw", "flamehunter", "shadowfang", 
        "dragonheart", "nightstorm", "warstorm", "ironshadow", "stormchaser", "lightstrike", "blademaster", 
        "dragonstrike", "phantomnight", "venomshade", "flameclash", "shadowpunch", "icefury", "soulhunter", 
        "nightfang", "frostbite", "cyberwarrior", "blazeaxe", "nightstrike", "stormbringer", "dragontamer", 
        "crimsonshadow", "shadowfire", "bloodshadow", "firehawk", "steelstorm", "nightwraith", "stormguard", 
        "wildstrike", "venomrider", "fireclaw", "moonfire", "shadowstrike", "sunflare", "vortexstrike", 
        "shadowflame", "dragonsoul", "bloodflare", "lightningblade", "tigerstorm", "venomstrike", "soulflare",
        "thunderwhisper", "necroticstorm", "pyroclash", "voidreaperx", "lucidflare", "darkvortex", "stealthblade",
        "thunderflare", "roguereaper", "darkstormx", "venomstrike", "redstorm", "blazingsun", "thundersoul",
        "flamerealm", "icyblaze", "smokephantom", "redphoenix", "duskflame", "nightdeath", "vortexvenom", 
        "goldenghost", "silentfury", "voidstrike", "ravenviper", "infinityblaze", "spiritualflame", 
        "frostshadow", "typhoonrider", "flameviper", "stormragex", "nightslayer", "deathclaw", "silentfang", 
        "thunderbolt", "stormshield", "blazedancer", "phantomghost", "moonhunter", "shadowwhisper", 
        "phoenixfire", "darkfang", "mysticshadow", "ironwhisper", "shadowphantom", "thunderstrikex", 
        "stormbringerx", "ragingflame", "coldblaze", "starphoenix", "icevenom", "moonfury", "silentreaper", 
        "shadowhunterx", "blazecreek", "voidblaze", "viperwolf", "frostraider", "soulseeker", "nightfall", 
        "lightningfang", "froststrike", "crimsonshade", "darkchaser", "firewarrior", "shadowseer", "cloudflare", 
        "phantomsoul", "redfang", "shadowstrikex", "cloudrider", "deathpunch", "windbreaker", "nightstrikex", 
        "vortexkiller", "icyclash", "soulflarex", "ironreaper", "blazehunter", "darkclash", "stormhunter", 
        "thunderflame", "nightsworn", "flamestrike", "venomstorm", "darkreign", "lightshadow", "frostwraith", 
        "galeclash", "dragonscorch", "hellfire", "stormsoul", "flamefuryx", "voidflame", "thunderdance", 
        "firewraith", "flameseeker", "moonvenom", "nightflare", "phantomclaw", "stormwrath", "lightbringerx", 
        "shadowblaze", "soulcrush", "thunderstrikez", "venomburn", "crimsonpunch", "darkvenom", "soulburner", 
        "lightningwing", "flamereaver", "nightshard", "vortexcurse", "phantomstorm", "blazeflare", "ironshadowx",
        "shadowfangx", "darkwarrior", "flameblood", "lightningwhisper", "icephoton", "soulwarrior", "nightfangx",
        "stormstrikez", "cyberblaze", "soulphantom", "frostflame", "darklight", "shadowflair", "venomstrikez", 
        "lightningprince", "silentfuryx", "blazevenom", "vortexflame", "fireangel", "soulphoenix", "icyreaper", 
        "dragonslash", "shadowwhisperx", "nightstormx", "lightningblaze", "phantomclash", "nightflarex", 
        "stormbreak", "darkstrike", "crimsonflame", "bloodflame", "icystrike", "stormflare", "redflame", 
        "thunderstrikez", "ghostflame", "darkphoenixx", "soulstrikez", "blazeclash", "thundergale", "shadowphantomx"]
    ])
    numeric=list('1234567890')
    special_char=list("~`!@#$%^&*.")
    style_default=('Alpha',0)
    premods_default='Gaming_ID'
    def __init__(self, password_lenght_limit: Tuple[int, int], style: Union[Tuple[Literal['AlphaNumeric', 'Alpha', 'Numeric'], int], None] = None, special_chars: bool = False, premods: Literal['Fruits','Vegetables','Flowers','Animals','Movies','Celebrities','Anime_Characters','Gaming_ID'] = None):
        self.premods = premods
        self.premods_default = premods if premods is not None else self.premods_default  # Default premod if None is provided
        self.style_default = style if style is not None else self.style_default
        
        self.classifier={'Fruits':self.fruits,'Flowers':self.flowers,'Animals':self.animals,'Movies':self.movies,
                         'Celebrities':self.celebrities,'Anime_Characters':self.anime_characters,'Gaming_ID':self.gaming_ids}
        
        self.temp_password_container=[]
        # Validate the password length limit (min, max)
        if isinstance(password_lenght_limit, tuple) and len(password_lenght_limit) == 2 and password_lenght_limit[1]-password_lenght_limit[0]>=4:
            if special_chars is False:
                # print('Special characters not allowed.')
                # print(self.style_default)
                # print(self.premods_default)
                
                if isinstance(self.style_default, tuple) and isinstance(self.style_default[1],int) and len(self.style_default)==2:
                    if self.style_default[0].lower() == 'alphanumeric':
                        self.min=password_lenght_limit[0]
                        self.max= password_lenght_limit[1]
                        self.num=self.style_default[1]
                        
                        if self.max-self.min <= self.num  :
                            raise ValueError(f"Length of the digits can't be more than or equal to password lenght,here password length: {self.max-self.min} and digit length: {self.num}")

                        elif self.num == 0:
                            self.password_list=self.classifier.get(self.premods_default)        
                            for self.row in self.password_list:
                                for self.value in self.row:
                                    # print(self.value)
                                    if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                        self.temp_password_container.append(self.value)
                            self.got_password= random.choice(self.temp_password_container)
                        else:
                            self.pre_num=random.choices(self.numeric, k=self.num)
                            self.end_val=self.max - self.num
                            self.password_list=self.classifier.get(self.premods_default)        
                            for self.row in self.password_list:
                                for self.value in self.row:
                                    # print(self.value)
                                    if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                        self.temp_password_container.append(self.value)
                            try:       
                                self.pre_password = random.choice(self.temp_password_container)
                                self.final_password = self.pre_password[0:self.end_val] + ''.join(self.pre_num)
                                self.got_password= self.final_password
                            except IndexError:
                                print("Can't generate password! Minimize the minimum lenght or try diffrent premods>>")
                                self.got_password=None
                            
                        
                        # print(self.style_default[0],'10000')
                    elif self.style_default[0].lower() == 'alpha':
                        self.password_list=self.classifier.get(self.premods_default)        
                        for self.row in self.password_list:
                            for self.value in self.row:
                                # print(self.value)
                                if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                    self.temp_password_container.append(self.value)
                        try:            
                            self.got_password= random.choice(self.temp_password_container)
                        except IndexError:
                            print("Can't generate password! Minimize the minimum lenght or try diffrent premods>>")
                            self.got_password=None
                    elif self.style_default[0].lower() == 'numeric':
                        self.pre_num_pass=random.choices(self.numeric, k=self.style_default[1])
                        self.got_password= ''.join(self.pre_num_pass)
                        # print(self.style_default[0])
                    else:
                        raise ValueError("No such option available!---->",self.style_default[0])
                else:
                    raise ValueError("'Style' accepts a tuple in the format: ('AlphaNumeric' or 'Alpha' or 'Numeric', digits lenght(int))")
            else:
                # print('Special characters allowed.')
                # print(self.style_default)
                # print(self.premods_default)
                if isinstance(self.style_default, tuple) and isinstance(self.style_default[1],int) and len(self.style_default)==2:
                    if self.style_default[0].lower() == 'alphanumeric':
                        self.min=password_lenght_limit[0]
                        self.max= password_lenght_limit[1]
                        self.num=self.style_default[1]
                        
                        if self.max-self.min <= self.num  :
                            raise ValueError(f"Length of the digits can't be more than or equal to password lenght,here password length: {self.max-self.min} and digit length: {self.num}")

                        elif self.num == 0:
                            self.password_list=self.classifier.get(self.premods_default)        
                            for self.row in self.password_list:
                                for self.value in self.row:
                                    # print(self.value)
                                    if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                        self.temp_password_container.append(self.value)
                            self.got_password= random.choice(self.temp_password_container)+random.choice(self.special_char)
                        else:
                            self.pre_num=random.choices(self.numeric, k=self.num)
                            self.end_val=self.max - self.num
                            self.password_list=self.classifier.get(self.premods_default)        
                            for self.row in self.password_list:
                                for self.value in self.row:
                                    # print(self.value)
                                    if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                        self.temp_password_container.append(self.value)
                            try:
                                self.pre_password = random.choice(self.temp_password_container)
                                self.final_password = self.pre_password[0:self.end_val] + ''.join(self.pre_num)
                            
                                self.got_password= self.final_password+random.choice(self.special_char)
                            except IndexError:
                                print("Can't generate password! Minimize the minimum lenght or try diffrent premods>>")
                                self.got_password=None
                            
                        
                        # print(self.style_default[0],'10000')
                    elif self.style_default[0].lower() == 'alpha':
                        self.password_list=self.classifier.get(self.premods_default)        
                        for self.row in self.password_list:
                            for self.value in self.row:
                                # print(self.value)
                                if len(self.value)>=password_lenght_limit[0] and len(self.value)<=password_lenght_limit[1]:
                                    self.temp_password_container.append(self.value)
                        try:
                            self.got_password= random.choice(self.temp_password_container)+random.choice(self.special_char)
                        except IndexError:
                            print("Can't generate password! Minimize the minimum lenght or try diffrent premods>>")
                            self.got_password=None
                        
                    elif self.style_default[0].lower() == 'numeric':
                        self.pre_num_pass=random.choices(self.numeric, k=self.style_default[1])
                        self.got_password=''.join(self.pre_num_pass)+random.choice(self.special_char)
                        # print(self.style_default[0])
                    else:
                        raise ValueError("No such option available!--->",self.style_default[0])
                else:
                    raise ValueError("'Style' accepts a tuple in the format: ('AlphaNumeric' or 'Alpha' or 'Numeric', digits lenght(int))")
        else:
            raise ValueError("'password_lenght_limit' accepts a tuple in the format: (min, max) with minimum lenght of 4")
        
    def get_password(self):
        return self.got_password
    
    
    
class AdvanceSecurity:
    base_algorithm = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J',
                 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T',
                 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
    
    state_symbol = {
                'andhra pradesh': 'AP', 'arunachal pradesh': 'AR', 'assam': 'AS', 'bihar': 'BR', 
                'chhattisgarh': 'CG', 'goa': 'GA', 'gujarat': 'GJ', 'haryana': 'HR', 
                'himachal pradesh': 'HP', 'jharkhand': 'JH', 'karnataka': 'KA', 'kerala': 'KL', 
                'madhya pradesh': 'MP', 'maharashtra': 'MH', 'manipur': 'MN', 'meghalaya': 'ML', 
                'mizoram': 'MZ', 'nagaland': 'NL', 'odisha': 'OD', 'punjab': 'PB', 
                'rajasthan': 'RJ', 'sikkim': 'SK', 'tamilnadu': 'TN', 'telangana': 'TG', 
                'tripura': 'TR', 'uttar pradesh': 'UP', 'uttarakhand': 'UK', 'west bengal': 'WB',
                'andaman and nicobar islands': 'AN', 'chandigarh': 'CH', 'dadra and nagar haveli and daman and diu': 'DN', 
                'lakshadweep': 'LD', 'delhi': 'DL', 'puducherry': 'PY'}
    
    specialchar = ['@', '#', '$', '*']
    age_default=[12, 21, 20, 18, 16, 60, 30]
    algorithm_default="algorithm1"
    

    emoji_list = ['😀', '🎉', '🚀', '✨', '🔥', '🌟', '🍀', '😍', '😎', '🤩']

    def __init__(self, username, area_code , state , age =None, algorithm : Literal['algorithm1', 'algorithm2', 'algorithm3', 'algorithm4'] = None):
        self.age_default = age if age is not None else random.choice(self.age_default)
        self.algorithm_default = algorithm if algorithm is not None else self.algorithm_default
        
        if isinstance(username, str) and len(username)>4:
            if algorithm == 'algorithm1':
                self.algorithm1( username)
            elif algorithm == 'algorithm2':
                self.algorithm2(username,state) 
            elif algorithm == 'algorithm3':
                self.algorithm3(username=username, state=state)
            elif algorithm == 'algorithm4':
                self.algorithm4(username, state, age)     
            else:
                print("Notice : The algorithm you requested doesn't exist or under development!")
        else:
            raise ValueError("Expected length of username>4.")

    
    def algorithm1(self, username):
        if ' ' not in username:
            self.new_name_str=username
            self.name_len = len(username)
            # print(self.name_len)
        else:
            self.new_name_str=''
            self.name_list=list(username)
            for self.spaces in self.name_list:
                if self.spaces != ' ':
                    self.new_name_str = self.new_name_str + self.spaces
            
            self.name_len = len(self.new_name_str)
            # print(self.name_len)
        
        self.new_username = self.new_name_str.lower()
        
        self.cap_math= (self.name_len*30)/100
        # print(self.cap_math)
        self.total_cap = math.floor(self.cap_math) + 1
        # print(self.total_cap)
        while True:
            self.cap_indexing = random.choices(range(0, self.name_len), k=self.total_cap)
            self.if_duplicate = len(self.cap_indexing) != len(set(self.cap_indexing))
            if self.if_duplicate is True:
                continue
            else:
                break
        # print(self.cap_indexing)
        # print(self.new_username)
        
        self.new_username_list = list(self.new_username)

        for self.index in self.cap_indexing:
            self.new_username_list[self.index] = self.new_username_list[self.index].upper()
        
        self.new_username = ''.join(self.new_username_list)
        
        # print(self.new_username)
        
        self.got_password_adv = self.new_username + str(self.age_default) + random.choice(self.specialchar)
        
    def algorithm2(self, username, state): 
        
        '''
        
        Algorithm2 is contributed by Pooja Velmurugen for more info : --> package().contributors
        
        
        '''

        self.username_clean = ''.join(username.split()).lower()  # Remove spaces and lowercase
        self.name_len = len(self.username_clean)

        self.random_caps = ''.join(char.upper() if random.choice([True, False])
                                    else char for char in self.username_clean)
        
    
        self.encoded_with_emojis = ''.join(random.choice(self.emoji_list) if char in 'aeiou'
                                           else char for char in self.random_caps)
        # print(self.encoded_with_emojis)
        
    
        state_code = self.state_symbol.get(state.lower(), "XX")
    
        self.got_password_adv = (self.encoded_with_emojis+ random.choice(self.emoji_list)+ state_code.upper()
                                 + str(self.age_default) + random.choice(self.specialchar) ) 
      
    
    def algorithm3(self, username,state):
        if ' ' not in username:
            self.new_name_str = username
            self.name_len = len(username)
        else:
            self.new_name_str = ''
            self.name_list = list(username)
            for self.spaces in self.name_list:
                if self.spaces != ' ':
                    self.new_name_str = self.new_name_str + self.spaces

            self.name_len = len(self.new_name_str)

        self.user_cap = self.new_name_str.upper()
        self.user_shape1 = []
        self.indement = [-2, 2]

        for self.k in self.user_cap:
            self.letter_num = [k for k, v in self.base_algorithm.items() if v == self.k]
            self.indement_val = random.choice(self.indement)
            self.final_indement = self.letter_num[0] + self.indement_val

            # Wrap the final_indement to be within the valid range [1, 26]
            if self.final_indement <= 0:
                self.final_indement = 26  # Wrap around to 'Z'
            elif self.final_indement > 26:
                self.final_indement = 1  # Wrap around to 'A'

            self.final_indement_val = self.base_algorithm[self.final_indement]
            self.user_shape1.append(self.final_indement_val)

        # print(''.join(self.user_shape1))
        self.adv_algo_name = ''.join(self.user_shape1)
        
        self.new_username_adv = self.adv_algo_name.lower()
        
        self.cap_math= (self.name_len*30)/100
        # print(self.cap_math)
        self.total_cap = math.floor(self.cap_math) + 1
        # print(self.total_cap)
        while True:
            self.cap_indexing = random.choices(range(0, self.name_len), k=self.total_cap)
            self.if_duplicate = len(self.cap_indexing) != len(set(self.cap_indexing))
            if self.if_duplicate is True:
                continue
            else:
                break
        # print(self.cap_indexing)
        # print(self.new_username_adv)
        
        self.new_username_list = list(self.new_username_adv)

        for self.index in self.cap_indexing:
            self.new_username_list[self.index] = self.new_username_list[self.index].upper()
        
        self.new_username_adv = ''.join(self.new_username_list)
        
        # print(self.new_username_adv)
        
        self.state_lower = state.lower()

        try:
            self.state_code = self.state_symbol[self.state_lower]
        except (ValueError, KeyError):
            self.state_code = "MP"
        
        self.got_password_adv = self.new_username_adv + str(self.age_default) + self.state_code +random.choice(self.specialchar)


    def algorithm4(self,username,state,age=None):
        
        if age is None:
            age = 18  
        try:
            age = int(age)  
        except ValueError:
            age = 18  
        
        self.name_cleaned = username.replace(" ", "").upper()

        self.name_unique = ""
        for char in self.name_cleaned:
            if char not in self.name_unique:
                self.name_unique += char

        self.name_sorted = "".join(sorted(self.name_unique))

        self.name_length = len(self.name_sorted)
        if self.name_length > 1:
            self.index_25 = math.floor(0.25 * self.name_length)
            self.index_75 = math.floor(0.75 * self.name_length)

            self.name_list = list(self.name_sorted)
            self.name_list[self.index_25] = self.name_list[self.index_25].lower()
            self.name_list[self.index_75] = self.name_list[self.index_75].lower()
            self.final_name = "".join(self.name_list)
        else:
            self.final_name = self.name_sorted

        self.half_length = self.name_length // 2
        self.final_name = self.final_name[:self.half_length] + self.final_name[self.half_length:][::-1]

               
        self.random_specialchar = random.choice(self.specialchar)

        self.name_count = len(self.final_name)
        self.age_increament= age + self.name_count

         
        self.state_lower = state.lower()

        try:
            self.state_code = self.state_symbol[self.state_lower]
        except (ValueError, KeyError):
            self.state_code = "MP" 
        
        #state_code = self.state_symbol.get(state, "XX")  
        self.state_code_with_age = f"{self.state_code[:1]}{self.age_increament}{self.state_code[1:]}"  

        self.got_password_adv = self.final_name + self.random_specialchar + self.state_code_with_age
      
      
    def get_password(self):
        return self.got_password_adv
        
        
class package:
    def __init__(self):
        init(autoreset=True)

    def help(self):
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\nFeatures:")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "1) " + Fore.GREEN + Back.BLACK + Style.NORMAL + "BasicSecurity")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "2) " + Fore.GREEN + Back.BLACK + Style.NORMAL + "AdvanceSecurity\n")

        print(Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "Demo : BasicSecurity -->")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "var1 = " + Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "BasicSecurity" + Fore.WHITE + Back.BLACK + Style.NORMAL + "(password_lenght_limit=(5,10), style=('alpha',0), special_chars=True, premods='Anime_Characters')")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "passs = " + Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "var1.get_password()" + Fore.WHITE + Back.BLACK + Style.NORMAL)
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "-------------------------------------------------------------------------------\n")
        
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "password_lenght_limit= " + Fore.WHITE + Back.BLACK + Style.NORMAL + "it accepts minimum and maximum length of desired password in tuple format with minimum gap of 4")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "style= " + Fore.WHITE + Back.BLACK + Style.NORMAL + "('format', format count)\n\t format have the options: " + Fore.CYAN + Back.BLACK + Style.NORMAL + "'alpha', 'alphanumeric', 'numeric'")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "\t format count: accepts length of digits in alphanumeric and numeric password")

        print(Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "\nExample:")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "If style=('alphanumeric', 3), it means the password will have 3 digits in it, while the rest will be alphabetic characters.")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\nspecial_chars: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "A boolean value (True or False) to indicate whether special characters should be allowed in the password.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "If special_chars=True, the generated password will include special characters.")
        
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\npremods: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "This is the category of pre-modified word list to use when generating passwords.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "Options include:")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Fruits' - Fruits list for generating passwords")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Vegetables' - Vegetables list")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Flowers' - Flowers list")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Animals' - Animals list")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Movies' - Movie titles")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Celebrities' - Celebrity names")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Anime_Characters' - Anime character names")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "\t'Gaming_ID' - Gaming usernames or IDs")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "Choose the one that suits the desired premod style of your password.")
        
        print(Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "\n\nDemo : AdvanceSecurity -->")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "var2 = " + Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "AdvanceSecurity" + Fore.WHITE + Back.BLACK + Style.NORMAL + "(username='johnDoe', area_code='1234', state='karnataka', age=25, algorithm='algorithm1')")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "pass_adv = " + Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "var2.get_password()" + Fore.WHITE + Back.BLACK + Style.NORMAL)
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "-------------------------------------------------------------------------------\n")

        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "username: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "A string that represents the user's username. The length should be greater than 4 characters.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "  - Example: 'johnDoe' (valid), 'j' (invalid, must be >4 characters).")
        
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\narea_code: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "A string representing the area code (e.g., '1234'). It is part of the username-generation process.")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\nstate: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "A string representing the state where the user resides. It should be one of the predefined states (e.g., 'karnataka').")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "  - States are matched with abbreviations from the state_symbol dictionary.")

        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\nage: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "(Optional) An integer representing the user's age. If not provided, a random age is selected from the predefined default age list.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "  - Default age choices are: [12, 21, 20, 18, 16, 60, 30].")

        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\nalgorithm: " + Fore.WHITE + Back.BLACK + Style.NORMAL + "(Optional) The algorithm used to generate the password. It accepts one of the following:")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "  - 'algorithm1' " + Fore.WHITE + Back.BLACK + Style.NORMAL + "(default algorithm if none is provided)")
        print(Fore.CYAN + Back.BLACK + Style.BRIGHT + "  -  algorithms (algorithm4) is placeholder and not yet implemented.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "  - 'algorithm1' generates a password by taking the username, removing spaces, converting it to lowercase, and then applying random uppercase transformations.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "    The password is further appended with the user's age and a random special character from the predefined set ['@', '#', '$', '*'].")

        print(Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "\nExample of password generation:")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "If the username is 'johnDoe', age is 25, and the selected algorithm is 'algorithm1',")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "the generated password could be something like 'JOHNDOE25@' where 'JOHNDOE' is the username transformed.")
        
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "\nNotes:")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "1) If no algorithm is provided, 'algorithm1' will be used by default.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "2) If the username contains spaces, they will be removed before processing.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "3) The number of uppercase characters in the final password is calculated based on the length of the username.")
        print(Fore.WHITE + Back.BLACK + Style.NORMAL + "4) Ensure that the username is longer than 4 characters; otherwise, a ValueError will be raised.")

        print(Fore.MAGENTA + Back.BLACK + Style.BRIGHT + "\nAdvanced features (algorithms 4) is placeholder and under development.")
    
    
    def contributors(self):
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Youraj Verma: ")
        print(Fore.CYAN + Back.BLACK + Style.NORMAL + "GitHub Link:" + Fore.WHITE + Back.BLACK + Style.NORMAL + " https://github.com/codex-yv")
        print(Fore.CYAN + Back.BLACK + Style.NORMAL + "Email:" + Fore.WHITE + Back.BLACK + Style.NORMAL + " yourajverma960@gmail.com")
        print(Fore.CYAN + Back.BLACK + Style.NORMAL + "------------------------------------------------------------------------------------")
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Pooja Velmurugen :")
        print(Fore.CYAN + Back.BLACK + Style.NORMAL + "GitHub Link:" + Fore.WHITE + Back.BLACK + Style.NORMAL + " https://github.com/Pooja-Velmurugen")
        print(Fore.CYAN + Back.BLACK + Style.NORMAL + "Email:" + Fore.WHITE + Back.BLACK + Style.NORMAL + " NOT AVAILABLE ")