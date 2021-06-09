import transform, predict

events = ['m200', 'f200', 'm100', 'f100']
for event in events:
    transform.transform(event)
    predict.run(event)