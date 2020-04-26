class SmellValidator(object):

    def validate_smell(self, validation_smells, existing_smells):
        # check validation smell
        for smell in validation_smells.cyclic_dependencies:
            matches = 0
            for existing_smell in existing_smells.cyclic_dependencies:
                for component in smell.participating_components:
                    for existing_component in existing_smell.participating_components:
                        if component.name == existing_component.name:
                            matches += 1
            print("Found %d matches for smell with id %s" % (matches, smell.id))
