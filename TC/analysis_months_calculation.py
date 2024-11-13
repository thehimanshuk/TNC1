
from logging import config
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta



def analyis_initial_months(event_date,pre_start,post_end,pre_end):

        pre_period_start = datetime.strptime(pre_start, '%b-%Y')
        event_start_date=event_date
        event_date = datetime.strptime(event_date, '%b-%Y')
        pre_end=datetime.strptime(pre_end, '%b-%Y')
        post_period_start = event_date
        post_period_end= datetime.strptime(post_end, '%b-%Y')

        delta_pre = relativedelta(pre_end, pre_period_start)
        delta_post = relativedelta(post_period_end, post_period_start)
        # Calculate the total number of months
        total_months_pre = delta_pre.years * 12 + delta_pre.months+1
        total_months_post=delta_post.years * 12 + delta_post.months+1
        pre_post_data={'pre_period_start':pre_period_start,
                   'pre_period_end':pre_end,
                   'post_period_start':post_period_start,
                   'post_period_end':post_period_end,
                   'total_months_pre':total_months_pre,
                   'total_months_post':total_months_post,
                   'event_date':event_start_date.replace(f'-{event_start_date.split("-")[-1]}', f'{int(event_start_date.split("-")[-1]) % 100}')}
        return pre_post_data
