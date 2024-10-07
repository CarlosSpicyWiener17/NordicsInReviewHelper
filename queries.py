TOURNAMENT_ENTRANTS = """query EventStandings($eventSlug: String!, $page: Int!) {
  event(slug: $eventSlug) {
    tournament {
      name
    }
    startAt
    entrants(query: {
      perPage: 50,
      page: $page}){
      pageInfo {
        totalPages
      }
      nodes {
          id
          name
          initialSeedNum
        	standing {
            placement
          }
        }
      }
    }
  }

"""