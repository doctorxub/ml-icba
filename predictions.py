classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

diseases_list = [
    {
        'id': 1,
        'title': 'Cucumber',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': [
            'Angular, pale yellow patches delineated by leaf veins.',
            'Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.',
            'Plants stunted, lack vigor, and die.'
        ],
        'control': [
            'Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds',
            'Spray Mancozeb 0.25% or Matalaxyl 0.15%'
        ],
        'image': 'images/0.jpg'
    },
    {
        'id': 2,
        'title': 'Cucumber',
        'type': 'Potassium (K)',
        'disease': 'Nutrient Deficiency',
        'sci': '',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': [
            'Older leaves may wilt, look scorched.',
            'Interveinal chlorosis begins at the base, scorching inward from leaf margins.'
        ],
        'control': [
            'Fertilizer with NPK'
        ],
        'image': 'images/1.jpg'
    },
    {
        'id': 3,
        'title': 'Cucumber',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': [
            'Tiny insects usually found on the back of leaves.',
            'Range in color from red and brown to yellow and green',
            'Produce webbing, when occur in high population, similar to the spiders',
            'Infected leaves appear discolored with pale dots, become scorched and drop.'
        ],
        'control': [
            'Spray Dicofol 18.5 EC @ 2000 ml/ha'
        ],
        'image': 'images/2.jpg'
    },
    {
        'id': 4,
        'title': 'Pepper',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': [
            'Angular, pale yellow patches delineated by leaf veins.',
            'Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.',
            'Plants stunted, lack vigor, and die.'
        ],
        'control': [
            'Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds',
            'Spray Mancozeb 0.25% or Matalaxyl 0.15%'
        ],
        'image': 'images/3.jpg'
    },
    {
        'id': 5,
        'title': 'Pepper',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': [
            'Tiny insects usually found on the back of leaves.',
            'Range in color from red and brown to yellow and green.',
            'Produce webbing, when occur in high population, similar to the spiders.',
            'Infected leaves appear discolored with pale dots, become scorched and drop.'
        ],
        'control': [
            'Spray Dicofol 18.5 EC @ 2000 ml/ha'
        ],
        'image': 'images/4.jpg'
    },
    {
        'id': 6,
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Early Blight',
        'sci': 'Alternaria solani',
        'hosts': 'Solanaceous vegetables (tomato, potato, pepper)',
        'symptoms': [
            'Brown to black spots on older leaves, enlarging and developing into concentric rings giving them a ‘target-spot’ appearance.',
            'Heavily infected leaves dry up and drop.',
            'Fruit lesions large with characteristic concentric rings.'
        ],
        'control': [
            'Seed treatment with (Carboxyn 37.5% + Thiram 37.5%) or Carbendazim DS @ 1.5 g/kg of seeds',
            'Foliar spray Mancozeb 0.25) or (Carbendazim 12% +Mancozeb 63%) @ 0.2%'
        ],
        'image': 'images/5.jpg'
    },
    {
        'id': 7,
        'title': 'Tomato',
        'type': 'Healthy',
        'disease': 'No identifiable disease detected',
        'sci': '',
        'hosts': 'Healthy Plant',
        'symptoms': [],
        'control': [],
        'image': 'images/6.jpg'
    },
    {
        'id': 8,
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Leaf Mold',
        'sci': 'Passalora fulva',
        'hosts': 'Tomatoes',
        'symptoms': [
            'Symptoms start as pale green to yellowish spots on upper leaf surfaces that turn a bright yellow.',
            'The spots merge as the disease progresses and the foliage then dies. Infected leaves curl, wither, and often drop from the plant.',
            'Flowers, stems, and fruit may be infected, although usually only leaf tissue is affected.',
            'When the disease does manifest on the fruit, tomatoes with leaf mold become dark in color, leathery, and rot at the stem end.'
        ],
        'control': [
            'Control relative humidity by venting greenhouse and pruning.',
            'Labeled fungicides may help control it.'
        ],
        'image': 'images/7.jpg'
    },
    {
        'id': 9,
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Powdery Mildew',
        'sci': 'Erysiphe spp, Sphaerotheca spp',
        'hosts': 'Affect all kinds of plants: cereals and grasses, vegetables, ornamentals and fruit trees, broad-leaved shade and forest trees',
        'symptoms': [
            'Spots or patches of white to grayish, talcum-powder like growth - mostly on the upper sides of the leaves.',
            'Can also affect the bottom sides of leaves, young stems, buds, flowers, and young fruit.'
        ],
        'control': [
            'Spary Dinocap 0.2% or Tridemorph 0.1% or Chlorothalonil 0.15% or Hexaconazole 0.1% or Wettable sulphur 0.3%'
        ],
        'image': 'images/8.jpg'
    },
]

deprecate_predictions = [
    {
        'title': 'Cucumber',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': '''<ul>
            <li>Angular, pale yellow patches delineated by leaf veins.</li>
            <li>Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.</li>
            <li>Plants stunted, lack vigor, and die.</li>
        </ul>''',
        'control': '''<ul>
            <li>Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds</li>
            <li>Spray Mancozeb 0.25% or Matalaxyl 0.15%</li>
        </ul>''',
        'image': 'images/0.jpg'
    },
    {
        'title': 'Cucumber',
        'type': 'Potassium (K)',
        'disease': 'Nutrient Deficiency',
        'sci': '',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': '''<ul>
            <li>Older leaves may wilt, look scorched.</li>
            <li>Interveinal chlorosis begins at the base, scorching inward from leaf margins.</li>
        </ul>''',
        'control': '''<ul>
            <li>Fertilizer with NPK</li>
        </ul>''',
        'image': 'images/1.jpg'
    },
    {
        'title': 'Cucumber',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': '''<ul>
            <li>Tiny insects usually found on the back of leaves.</li>
            <li>Range in color from red and brown to yellow and green</li>
            <li>Produce webbing, when occur in high population, similar to the spiders</li>
            <li>Infected leaves appear discolored with pale dots, become scorched and drop.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spray Dicofol 18.5 EC @ 2000 ml/ha</li>
        </ul>''',
        'image': 'images/2.jpg'
    },
    {
        'title': 'Pepper',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': '''<ul>
            <li>Angular, pale yellow patches delineated by leaf veins.</li>
            <li>Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.</li>
            <li>Plants stunted, lack vigor, and die.</li>
        </ul>''',
        'control': '''<ul>
            <li>Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds</li>
            <li>Spray Mancozeb 0.25% or Matalaxyl 0.15%</li>
        </ul>''',
        'image': 'images/3.jpg'
    },
    {
        'title': 'Pepper',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': '''<ul>
            <li>Tiny insects usually found on the back of leaves.</li>
            <li>Range in color from red and brown to yellow and green.</li>
            <li>Produce webbing, when occur in high population, similar to the spiders.</li>
            <li>Infected leaves appear discolored with pale dots, become scorched and drop.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spray Dicofol 18.5 EC @ 2000 ml/ha</li>
        </ul>''',
        'image': 'images/4.jpg'
    },
    {
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Early Blight',
        'sci': 'Alternaria solani',
        'hosts': 'Solanaceous vegetables (tomato, potato, pepper)',
        'symptoms': '''<ul>
            <li>Brown to black spots on older leaves, enlarging and developing into concentric rings giving them a ‘target-spot’ appearance.</li>
            <li>Heavily infected leaves dry up and drop.</li>
            <li>Fruit lesions large with characteristic concentric rings.</li>
        </ul>''',
        'control': '''<ul>
            <li>Seed treatment with (Carboxyn 37.5% + Thiram 37.5%) or Carbendazim DS @ 1.5 g/kg of seeds</li>
            <li>Foliar spray Mancozeb 0.25) or (Carbendazim 12% +Mancozeb 63%) @ 0.2%</li>
        </ul>''',
        'image': 'images/5.jpg'
    },
    {
        'title': 'Tomato',
        'type': 'Healthy',
        'disease': 'No identifiable disease detected',
        'sci': '',
        'hosts': 'Healthy Plant',
        'symptoms': '',
        'control': '',
        'image': 'images/6.jpg'
    },
    {
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Leaf Mold',
        'sci': 'Passalora fulva',
        'hosts': 'Tomatoes',
        'symptoms': '''<ul>
            <li>Symptoms start as pale green to yellowish spots on upper leaf surfaces that turn a bright yellow.</li>
            <li>The spots merge as the disease progresses and the foliage then dies. Infected leaves curl, wither, and often drop from the plant.</li>
            <li>Flowers, stems, and fruit may be infected, although usually only leaf tissue is affected.</li>
            <li>When the disease does manifest on the fruit, tomatoes with leaf mold become dark in color, leathery, and rot at the stem end.</li>
        </ul>''',
        'control': '''<ul>
            <li>Control relative humidity by venting greenhouse and pruning.</li>
            <li>Labeled fungicides may help control it.</li>
        </ul>''',
        'image': 'images/7.jpg'
    },
    {
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Powdery Mildew',
        'sci': '''Erysiphe spp.
        Sphaerotheca spp.''',
        'hosts': 'Affect all kinds of plants: cereals and grasses, vegetables, ornamentals and fruit trees, broad-leaved shade and forest trees',
        'symptoms': '''<ul>
            <li>Spots or patches of white to grayish, talcum-powder like growth - mostly on the upper sides of the leaves.</li>
            <li>Can also affect the bottom sides of leaves, young stems, buds, flowers, and young fruit.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spary Dinocap 0.2% or Tridemorph 0.1% or Chlorothalonil 0.15% or Hexaconazole 0.1% or Wettable sulphur 0.3%</li>
        </ul>''',
        'image': 'images/8.jpg'
    },
]
