BaseElement 
    -- Photo (Instagram)
    -- Tweet (Tweet)


BaseEvent 
    -- Event (equivalent to PhotoEvent)
        -- PhotoEvent (equivalent to Event except the relation)
    -- TweetEvent
    -- BaseFeature (all photo features are included here)
        -- BaseFeatureProduction (for production, photo)
        -- TwitterFeature


MongoDBInterface  
    -- ElementInterface (rangeQuery)
        -- PhotoInterface
        -- TweetInterface
    -- PredictionInterface
    -- EventInterface