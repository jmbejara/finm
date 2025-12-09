import finm

# Calculate bond price
price = finm.bond_price(
    face_value=1000,
    coupon_rate=0.06,    # 6% annual coupon
    ytm=0.05,            # 5% yield to maturity
    periods=10,          # 10 semi-annual periods (5 years)
    frequency=2          # Semi-annual payments
)
print(f"Bond Price: ${price:.2f}")

# Calculate present value
pv = finm.present_value(
    future_value=1000,
    rate=0.05,
    periods=2
)
print(f"Present Value: ${pv:.2f}")

# Calculate duration and convexity
dur = finm.duration(1000, 0.06, 0.05, 10, frequency=2)
mod_dur = finm.modified_duration(1000, 0.06, 0.05, 10, frequency=2)
conv = finm.convexity(1000, 0.06, 0.05, 10, frequency=2)

print(f"Macaulay Duration: {dur:.4f} years")
print(f"Modified Duration: {mod_dur:.4f}")
print(f"Convexity: {conv:.4f}")

# Get coupon payment dates
coupon_dates = finm.get_coupon_dates(
    quote_date="2020-01-01",
    maturity_date="2025-01-01",
)
print("Coupon Payment Dates:")
for date in coupon_dates:
    print(date.strftime("%Y-%m-%d"))

df_treas = finm.pull_CRSP_treasury_daily(
    start_date="2020-01-01",
    end_date="2020-12-31",
    wrds_username="jszajkowski",
)

df_treas.to_parquet("df_treas.parquet")

df_cons = finm.pull_CRSP_treasury_consolidated(
    start_date="2020-01-01",
    end_date="2020-12-31",
    wrds_username="jszajkowski",
)

df_cons.to_parquet("df_cons.parquet")
