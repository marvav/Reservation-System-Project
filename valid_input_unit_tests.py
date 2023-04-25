from Auxilary_Functions import *

if __name__ == '__main__':
    tour = {}
    assert not is_valid_tour(tour)
    tour["Name"]="Prohlídka"
    tour["Location"]="Brno"
    tour["Capacity"]="50"
    tour["Duration"]="50"
    tour["TicketPrice"]="50"
    tour["DiscountPrice"]="50"
    tour["Description"]=""
    assert is_valid_tour(tour)
    tour["Duration"]="-50"
    assert not is_valid_tour(tour)
    tour["Duration"]="0"
    assert not is_valid_tour(tour)
