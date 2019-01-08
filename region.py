"""
SOPHIE WASHINGTON
CS1103 PROJECT 4
29 November 2018

This file acts as the Model.

It takes lists of coordinates and a breakdown of vote counts
by party (republican, democrat and other) and then creates percentages
and lists in order to later feed into the 'plot' and 'election' files.
"""

import csv
import sys

class Region:
    """
    A region (represented by a list of long/lat coordinates) along with
    republican, democrat, and other vote counts.
    """
    def __init__(self, coords, r_votes, d_votes, o_votes):
        self.coordinates = coords
        self.republican_votes = r_votes
        self.democrat_votes = d_votes
        self.other_votes = o_votes


    def lats(self):
        "Return a list of the latitudes of all the coordinates in the region"
        lats = [x[1] for x in self.coordinates]
        return lats


    def longs(self):
        "Return a list of the longitudes of all the coordinates in the region"
        longs = [x[0] for x in self.coordinates]
        return longs


    def min_lat(self):
        "Return the minimum latitude of the region"
        return min(self.lats())


    def min_long(self):
        "Return the minimum longitude of the region"
        return min(self.longs())


    def max_lat(self):
        "Return the maximum latitude of the region"
        return max(self.lats())


    def max_long(self):
        "Return the maximum longitude of the region"
        return max(self.longs())


    def plurality(self):
        "Return 'REPUBLICAN','DEMOCRAT', or 'OTHER' depending on plurality of votes"
        vote_counts = [self.republican_votes, self.democrat_votes, self.other_votes]
        party_plurality = ""
        if max(vote_counts) == self.republican_votes:
            party_plurality = "REPUBLICAN"
        if max(vote_counts) == self.democrat_votes:
            party_plurality = "DEMOCRAT"
        if max(vote_counts) == self.other_votes:
            party_plurality = "OTHER"
        return party_plurality


    def total_votes(self):
        "The total number of votes cast in this region"
        total_votes = self.democrat_votes + self.republican_votes + self.other_votes
        return total_votes


    def republican_percentage(self):
        "The precentage of republication votes cast in this region"
        repub_percentage = self.republican_votes/self.total_votes()
        return repub_percentage


    def democrat_percentage(self):
        "The precentage of democrat votes cast in this region"
        dem_percentage = self.democrat_votes/self.total_votes()
        return dem_percentage


    def other_percentage(self):
        "The precentage of other votes cast in this region"
        oth_percentage = self.other_votes/self.total_votes()
        return oth_percentage



