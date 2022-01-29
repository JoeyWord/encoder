--访问信息与提交记录去重合并
create table own_reason_model_base_d_tmp_1 stored as rcfile as
select a.user_id,a.session_id,a.date as visit_date,a.time as visit_time,b.time as submit_time,
datediff(b.time,a.time) as delta_time,a.utm_term,a.utm_source,a.utm_medium
from 
(select user_id ,$session_id as session_id, date, time, utm_term,utm_source,utm_medium
      from sessions_session_user_behavior/*SESSION_TABLE_DATE_RANGE=[2018-10-01,2018-11-15]*/  
      where event = '$pageview' and $utm_term <> '' and is_login = 1) a
left join
(select user_id ,$session_id as session_id, date, time from 
(select user_id ,$session_id as session_id, date, time,
		row_number() over(distribute by user_id,$session_id,date sort by time) as rk 
      from sessions_session_user_behavior/*SESSION_TABLE_DATE_RANGE=[2018-10-01,2018-11-15]*/  
      where event = 'PaperSubmit' and is_login = 1 ) b
      where b.rk=1) bb
on a.user_id=bb.user_id and a.session_id=bb.session_id and a.date=bb.date
order by user_id,pageview_time;

--提交记录校正，并生成提交记录标识字段is_submit
create table own_reason_model_base_d_tmp_2 stored as rcfile as
select a.user_id,a.session_id,a.date as visit_date,a.pageview_time as visit_time
		a.utm_term,a.utm_source,a.utm_medium,case when b.delta_time is not null then 1 else 0 end as is_submit
from own_reason_model_base_d_tmp_1 a
left join(
			select bb.visit_time,bb.delta_time
			from (
					select user_id,session_id,visit_date,visit_time,delta_time,row_number()over(distribute by user_id,session_id,date sort by delta_time) as rn
					from own_reason_model_base_d_tmp_1
					where delta_time is not null
					)bb
			where bb.rn=1
			)b
on on a.visit_time=b.visit_time;

--合并消费金额
create table own_reason_model_base_d stored as rcfile as
select a.user_id,a.session_id,visit_date,a.visit_time
		a.utm_term,a.utm_source,a.utm_medium,a.is_submit,nvl(b.pay_amt,0.0) as pay_amt
from own_reason_model_base_d_tmp_2 a
left join(
			select user_id ,$session_id as session_id, date, sum(submit_amout) as 
					pay_amt
      		from sessions_session_user_behavior/*SESSION_TABLE_DATE_RANGE=[2018-10-01,2018-11-15]*/  
      		group by user_id,$session_id,date
		) b
on a.user_id=b.user_id and a.session_id=b.session_id and a.date=b.date;



