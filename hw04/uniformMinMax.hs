min :: Int -> Double -> Double -> Double -> Double
min n a b x | x <= a = 0
            | x >= b = 1
            | otherwise = 1 - (1 - (x - a) / (b - a)) ** (fromIntegral n)

max :: Int -> Double -> Double -> Double -> Double
max n a b x | x <= a = 0
            | x >= b = 1
            | otherwise = ((x - a) / (b - a)) ** (fromIntegral n)
