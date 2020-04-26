import operator


class SmellValidator(object):

    def validate_smell(self, validation_smells, existing_smells):
        # check cyclic dependencies
        for smell in validation_smells.cyclic_dependencies:
            match_list = dict()
            for existing_smell in existing_smells.cyclic_dependencies:
                matches = 0
                for component in smell.participating_components:
                    match = False
                    for existing_component in existing_smell.participating_components:
                        if component.name == existing_component.name:
                            match = True
                    if match:
                        matches += 1
                if matches >= 2:
                    match_list[existing_smell.id] = matches
            print("Found %d similar cycles for smell with id %s" % (len(match_list), smell.id))
            key = max(match_list.items(), key=operator.itemgetter(1))[0]
            print("The most similar cycle is id %s with %d matched components" % (key, match_list[key]))

