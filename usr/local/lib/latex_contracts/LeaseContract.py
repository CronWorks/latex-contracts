# /usr/bin/env python

# Copyright 2012, 2013, 2014 J. Luke Scott
# This file is part of latex-contracts.

# latex-contracts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# latex-contracts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with latex-contracts.  If not, see <http://www.gnu.org/licenses/>.


from latex_python.JinjaBase import JsonSerializable, Money, Percent
from Contract import Contract, Person, Address
from re import sub

class Lessor(Person):
    pass  # _required & __init__ are the same

class Tenant(Person):
    def __init__(self, **kwargs):
        self.forwardingAddress = Address()
        self.forwardingPhoneNumber = ''
        super(Tenant, self).__init__(**kwargs)

class Occupant(Person):
    pass  # _required & __init__ are the same

PROPERTY_ELEMENTS = {'appliances': 'Appliances',
                     'cleanliness':'Cleanliness',
                     'closet': 'Closet Space',
                     'sink': 'Sink and Faucet',
                     'sinkWithInsert': 'Sink, Sink Insert, and Faucet',
                     'countertops': 'Counter tops',
                     'tileCountertops': 'Tile counter tops',
                     'cupboards':'Cupboards, Drawers',
                     'electrical': 'Lights, Outlets',
                     'electricMeter': 'Electric Meter Reading',
                     'furniture': 'Any furniture owned by Lessor',
                     'general': 'General condition/damage',
                     'gasMeter': 'Gas Meter Reading',
                     'heatingOil': 'Heating Oil Level',
                     'shower': 'Shower and Surround',
                     'smokeDetectors': 'List any inoperable smoke detectors',
                     'toilet': 'Toilet',
                     'walls': 'Walls, Floors, Windows, Blinds',
                     'washer': 'Washer/Dryer',
                     'waterMeter': 'Water Meter Reading',
                     'weeding': 'Weeding and Mowing',
                     }

class SubjectToInspection(JsonSerializable):
    def __init__(self, **kwargs):
        self._inspectionItems = []  # items to attach to the room (subclass as appropriate)
        self._moveInConditions = {}
        self._moveOutConditions = {}
        super(SubjectToInspection, self).__init__(**kwargs)

    def setCondition(self, itemId, moveInOrOut, condition):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        if not conditionDict:
            setattr(self, '_%sConditions' % moveInOrOut, conditionDict)
        conditionDict[itemId] = condition

    def getConditionsTuples(self, moveInOrOut, ignoreList=[]):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        resultDict = {}
        for itemId in sorted(self._inspectionItems):
            if itemId in ignoreList:
                continue
            label = PROPERTY_ELEMENTS[itemId]
            condition = conditionDict.get(itemId, '')
            resultDict[label] = condition
        return [(label, resultDict[label]) for label in sorted(resultDict.keys())]

class Room(SubjectToInspection):
    def __init__(self, label=None, **kwargs):
        # shortcut instantiation syntax
        # if left empty, str(room) will return class name ('Bedroom')
        kwargs['label'] = label or ''
        super(Room, self).__init__(**kwargs)

    def __str__(self):
        # 'TheSpecialRoomClass' > 'The Special Room Class'
        roomType = sub(r'([A-Z])', r' \1', self.__class__.__name__).strip()
        return ('%s %s' % (self.label, roomType)).strip()

class Kitchen(Room):
    def __init__(self, label=None, tileCountertops=False, sinkWithInsert=False, **kwargs):
        super(Kitchen, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'sink',
                                 'countertops',
                                 'cupboards',
                                 'electrical',
                                 'furniture',
                                 'walls']
        if tileCountertops:
            i = self._inspectionItems.index('countertops')
            self._inspectionItems[i] = 'tileCountertops'
        if sinkWithInsert:
            i = self._inspectionItems.index('sink')
            self._inspectionItems[i] = 'sinkWithInsert'

class LivingRoom(Room):
    def __init__(self, label=None, tileCountertops=False, sinkWithInsert=False, **kwargs):
        super(LivingRoom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'electrical',
                                 'walls',
                                 'cupboards',
                                 'furniture',
                                 ]
        if tileCountertops:
            i = self._inspectionItems.index('countertops')
            self._inspectionItems[i] = 'tileCountertops'
        if sinkWithInsert:
            i = self._inspectionItems.index('sink')
            self._inspectionItems[i] = 'sinkWithInsert'

class Bedroom(Room):
    def __init__(self, label=None, **kwargs):
        super(Bedroom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'closet',
                                 'electrical',
                                 'furniture',
                                 'walls']

class Bathroom(Room):
    def __init__(self, label=None, **kwargs):
        super(Bathroom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'countertops',
                                 'electrical',
                                 'shower',
                                 'toilet',
                                 'walls']

class Deck(Room):  # not really a room, but close enough
    def __init__(self, label=None, **kwargs):
        super(Deck, self).__init__(**kwargs)
        self._inspectionItems = ['cleanliness',
                                 'furniture']

class Basement(Room):
    def __init__(self, **kwargs):
        super(Basement, self).__init__(**kwargs)
        self._inspectionItems = ['general']

class YardAndLawn(Room):
    def __init__(self, **kwargs):
        super(YardAndLawn, self).__init__(**kwargs)
        self._inspectionItems = ['cleanliness',
                                 'weeding']

class Property(SubjectToInspection):
    def __init__(self, **kwargs):
        self.clauses = {}  # format: {'sectionName': [clause list], ...}
        self.applicationFee = Money(35)
        self.depositNonRefundable = Money(250)
        self.furnished = False
        self.rooms = []
        self.roommateOnly = False
        self.tenantMaintainsYard = True
        self.utilitiesIncluded = []

        super(Property, self).__init__(**kwargs)

        self._required = ['address',
                          'county',
                          'rent',
                          'deposit',
                          'occupantLimit']

        # add gas/oil on a per-property basis
        self._inspectionItems = ['smokeDetectors',
                                 'electricMeter',
                                 ]


class LeaseContract(Contract):
    def __init__(self, templateModule=None, searchPath=None, signatureFilePath=None, **kwargs):
        self.lessors = []
        self.occupants = []
        self.tenants = []
        self.property = None

        self.leaseStartDate = None
        self.leaseEndDate = None
        self.monthToMonth = False
        self.renewal = False
        self.signSections = []

        self.moveInTime = '2:00pm'
        self.moveOutTime = '12:00pm (noon)'
        self.depositRefundGracePeriodDays = 14
        self.initialMaintenanceGracePeriodDays = 7
        self.paymentGracePeriodDays = 5
        self.possessionGracePeriodDays = 7
        self.moveInInspectionGracePeriodDays = 2
        self.securityDepositGracePeriodDays = 5
        self.dailyLatePenalty = Money(25)
        self.latePenaltyLimitPercent = Percent(10)
        self.bouncedCheckPenalty = Money(50)

        self.title = 'Lease/Rental Agreement'
        self.subtitle = "This document is a Lease Agreement (``Agreement'') between Lessor and Tenant for occupation of a residential property."

        super(LeaseContract, self).__init__(templateModule, searchPath, signatureFilePath, **kwargs)

        self._required += ['depositAccountBankName',
                           'depositAccountBankCityState']

    def getSigningPeople(self):
        return self.tenants + self.lessors

    def multipleTenants(self):
        return len(self.tenants) + len(self.occupants) > 1

    def getLessorDefinitions(self, i):
        label = 'Lessor'
        if len(self.lessors) > 1:
            # if we need ot distinguish multiple people, then say "Person 1" instead of "Person"
            label = '%s %d' % (label, i + 1)
        return self.getPersonDefinitions(label, self.lessors[i])

    def getTenantDefinitions(self, i):
        label = 'Tenant'
        if len(self.tenants) > 1:
            # if we need ot distinguish multiple people, then say "Person 1" instead of "Person"
            label = '%s %d' % (label, i + 1)
        return self.getPersonDefinitions(label, self.tenants[i])

    def getOccupantDefinitions(self, i):
        label = 'Occupant'
        if len(self.occupants) > 1:
            # if we need ot distinguish multiple people, then say "Person 1" instead of "Person"
            label = '%s %d' % (label, i + 1)
        return self.getPersonDefinitions(label, self.occupants[i])

    def getPersonDefinitions(self, label, person):
        result = ['\\definition{%s}{%s}'%(label, person.name)]
        if hasattr(person, 'address'):
            result.append('\\definition{%s address}{%s}' % (label, person.address.getFullAddressTex()))
        if hasattr(person, 'phone'):
            result.append('\\definition{%s telephone number}{%s}' % (label, person.phone))
        if hasattr(person, 'email'):
            result.append('\\definition{%s email address}{%s}' % (label, person.email))
        return '\n'.join(result)

    def getNumberOfFooterRows(self):
        numberOfInitialsRows = max(len(self.lessors), len(self.tenants))
        return 2 + numberOfInitialsRows  # 2 for "initials:" label and "page x of y"

    def getInspectionFormContent(self, moveInOrOut):
        result = self.getInspectionContent('General', self.property, moveInOrOut)
        for room in self.property.rooms:
            result += self.getInspectionContent(str(room), room, moveInOrOut)

        return '\n'.join(result)

    def getInspectionContent(self, label, thingToInspect, moveInOrOut):
        result = ['\\subsection{%s}' % label]
        ignoreList = []
        if not self.property.furnished:
            ignoreList.append('furniture')
        for (label, condition) in thingToInspect.getConditionsTuples(moveInOrOut, ignoreList):
            result.append('\\formLine[%s]{%s}' % (condition, label))
        return result

    def generate(self, outputFilename, system, variables={}):
        # override default clauses with property's custom clauses
        # will trigger template to be added if it hasn't been already
        for sectionName in self.property.clauses:
            for clause in self.property.clauses[sectionName]:
                self.addClause(sectionName, clause)
        super(LeaseContract, self).generate(outputFilename, system, variables)

