# Copyright [2013] Eddie Xie.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import photo_interface, tweet_interface


class TimeSeries(object):
    """For a single region specified by a box of
    [upper_left_lat, upper_left_lng, down_right_lat, down_right_lng]
    
    """

    def __init__(self, region, start_timestamp, end_timestamp, freq='1h', data_source='instagram'):
        self.sample_freq = freq
        self.freq = freq
        if data_source == 'instagram':
            pi = photo_interface.PhotoInterface()
            self.cursor = pi.rangeQuery(region, (str(start_timestamp), str(end_timestamp)))
        elif data_source == 'twitter':
            print 'in twitter!'
            pi = tweet_interface.TweetInterface('citybeat_production', 'tweets')
            region.display()
            self.cursor = pi.rangeQuery(region, [str(start_timestamp), str(end_timestamp)])
