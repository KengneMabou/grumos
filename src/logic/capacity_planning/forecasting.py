# coding: utf-8 
'''
Created on 16 sept. 2016

@author: kengne
'''
class GrumosForecastiong:
    
    def initial_trend(self, series, slen):
        trend_sum = 0.0
        for i in range(slen):
            trend_sum += float(series[i+slen] - series[i]) / slen
        return trend_sum / slen
    def initial_seasonal_components(self, series, slen):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(series)/slen)
        # compute season averages
        for j in range(n_seasons):
            season_averages.append(sum(series[slen*j:slen*j+slen])/float(slen))
        # compute initial values
        for i in range(slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += series[slen*j+i]-season_averages[j]
            seasonals[i] = sum_of_vals_over_avg/n_seasons
        return seasonals
    
    def additiveHoltWinters(self, series, slen, alpha, beta, gamma, n_preds):
        """
        This methode compute the "triple exponential smoothing" prevision algorithm also called
        This is the additive form of the method.
        It takes 6 arguments: the the past series observed (series), the season length (slen), the smoothing
        parameter (alpha, beta, gamma) and the number of point with want to forecast (n_preds)
        Testing values for α, β and γ : 0.716, 0.029 and 0.993 
        """
        
        result = []
        seasonals = self.initial_seasonal_components(series, slen)
        
        for i in range(len(series)+n_preds):
            if i == 0: # initial values
                smooth = series[0]
                trend = self.initial_trend(series, slen)
                result.append(series[0])
                continue
            if i >= len(series): # we are forecasting
                m = i - len(series) + 1
                result.append((smooth + m*trend) + seasonals[i%slen])
            else:
                val = series[i]
                last_smooth, smooth = smooth, alpha*(val-seasonals[i%slen]) + (1-alpha)*(smooth+trend)
                trend = beta * (smooth-last_smooth) + (1-beta)*trend
                seasonals[i%slen] = gamma*(val-smooth) + (1-gamma)*seasonals[i%slen]
                result.append(smooth+trend+seasonals[i%slen])
        return result



#===============================================================================
# import math
# from datetime import timedelta
# from src.business.capacity_planing.time_series import TimeSeries
# from src.logic.capacity_planning.evaluators import Evaluators
# 
# class Graphiteforecasting:
#     
#     def holtWintersForecast(self, requestContext, seriesList):
#         """
#         Performs a Holt-Winters forecast using the series as input data. Data from
#         one week previous to the series is used to bootstrap the initial forecast.
#         """
#         previewSeconds = 7 * 86400 # 7 days
#         # ignore original data and pull new, including our preview
#         newContext = requestContext.copy()
#         newContext['startTime'] = requestContext['startTime'] -  timedelta(seconds=previewSeconds)
#         previewList = Evaluators().evaluateTokens(newContext, requestContext['args'][0])
#         results = []
#         for series in previewList:
#             analysis = self.holtWintersAnalysis(series)
#             predictions = analysis['predictions']
#             windowPoints = previewSeconds / predictions.step
#             result = TimeSeries("holtWintersForecast(%s)" % series.name, predictions.start + previewSeconds, predictions.end, predictions.step, predictions[windowPoints:])
#             result.pathExpression = result.name
#             results.append(result)
#       
#         return results
#     
#     def holtWintersAnalysis(self,series):
#         alpha = gamma = 0.1
#         beta = 0.0035
#         # season is currently one day
#         season_length = (24*60*60) / series.step
#         intercept = 0
#         slope = 0
#         pred = 0
#         intercepts = list()
#         slopes = list()
#         seasonals = list()
#         predictions = list()
#         deviations = list()
#     
#         def getLastSeasonal(i):
#             j = i - season_length
#             if j >= 0:
#                 return seasonals[j]
#             return 0
#     
#         def getLastDeviation(i):
#             j = i - season_length
#             if j >= 0:
#                 return deviations[j]
#             return 0
#     
#         last_seasonal = 0
#         last_seasonal_dev = 0
#         next_last_seasonal = 0
#         next_pred = None
# 
#         for i,actual in enumerate(series):
#             if actual is None:
#                 # missing input values break all the math
#                 # do the best we can and move on
#                 intercepts.append(None)
#                 slopes.append(0)
#                 seasonals.append(0)
#                 predictions.append(next_pred)
#                 deviations.append(0)
#                 next_pred = None
#                 continue
#     
#             if i == 0:
#                 last_intercept = actual
#                 last_slope = 0
#                 # seed the first prediction as the first actual
#                 prediction = actual
#             else:
#                 last_intercept = intercepts[-1]
#                 last_slope = slopes[-1]
#                 if last_intercept is None:
#                     last_intercept = actual
#                 prediction = next_pred
#     
#             last_seasonal = getLastSeasonal(i)
#             next_last_seasonal = getLastSeasonal(i+1)
#             last_seasonal_dev = getLastDeviation(i)
#     
#             intercept = self.holtWintersIntercept(alpha,actual,last_seasonal,last_intercept,last_slope)
#             slope = self.holtWintersSlope(beta,intercept,last_intercept,last_slope)
#             seasonal = self.holtWintersSeasonal(gamma,actual,intercept,last_seasonal)
#             next_pred = intercept + slope + next_last_seasonal
#             deviation = self.holtWintersDeviation(gamma,actual,prediction,last_seasonal_dev)
#         
#             intercepts.append(intercept)
#             slopes.append(slope)
#             seasonals.append(seasonal)
#             predictions.append(prediction)
#             deviations.append(deviation)
#     
#         # make the new forecast series
#         forecastName = "holtWintersForecast(%s)" % series.name
#         forecastSeries = TimeSeries(forecastName, series.start, series.end, series.step, predictions)
#         forecastSeries.pathExpression = forecastName
#     
#         # make the new deviation series
#         deviationName = "holtWintersDeviation(%s)" % series.name
#         deviationSeries = TimeSeries(deviationName, series.start, series.end, series.step, deviations)
#         deviationSeries.pathExpression = deviationName
#     
#         results = { 'predictions': forecastSeries
#             , 'deviations': deviationSeries
#             , 'intercepts': intercepts
#             , 'slopes': slopes
#             , 'seasonals': seasonals
#         }
#         return results
#     
#     def holtWintersIntercept(self,alpha,actual,last_season,last_intercept,last_slope):
#         return alpha * (actual - last_season) + (1 - alpha) * (last_intercept + last_slope)
# 
#     def holtWintersSlope(self, beta,intercept,last_intercept,last_slope):
#         return beta * (intercept - last_intercept) + (1 - beta) * last_slope
# 
#     def holtWintersSeasonal(self, gamma,actual,intercept,last_season):
#         return gamma * (actual - intercept) + (1 - gamma) * last_season
# 
#     def holtWintersDeviation(self, gamma,actual,prediction,last_seasonal_dev):
#         if prediction is None:
#             prediction = 0
#         return gamma * math.fabs(actual - prediction) + (1 - gamma) * last_seasonal_dev
#===============================================================================
    
