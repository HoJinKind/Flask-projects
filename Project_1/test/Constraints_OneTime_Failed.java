

package Project;

import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;



public class Constraints_OneTime_Failed {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();
  boolean result;
  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void Constraints_OneTime_Invalid_StartTime() throws Exception {
	String user = "tom";
	String pwd= "sutd1234";
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    
    Thread.sleep(3000);
    driver.get("http://35.198.199.181:5000/constraint_OneTime");
    driver.findElement(By.name("eventName")).click();
    driver.findElement(By.name("eventName")).clear();
    driver.findElement(By.name("eventName")).sendKeys("CNY");
    driver.findElement(By.name("weekNo")).click();
    driver.findElement(By.name("weekNo")).clear();
    driver.findElement(By.name("weekNo")).sendKeys("5");
    driver.findElement(By.name("startTime")).click();
    driver.findElement(By.name("startTime")).clear();
    driver.findElement(By.name("startTime")).sendKeys("07:30");
    driver.findElement(By.name("endTime")).click();
    driver.findElement(By.name("endTime")).clear();
    
    driver.findElement(By.name("endTime")).sendKeys("18:00");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='End Time'])[1]/following::input[2]")).click();
    
    Thread.sleep(2000);
    assertEquals ("constraints_View", driver.getTitle());
  }

  @Test
  public void Constraints_OneTime_Invalid_EndTime() throws Exception {
	String user = "tom";
	String pwd= "sutd1234";
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    
    Thread.sleep(3000);
    driver.get("http://35.198.199.181:5000/constraint_OneTime");
    driver.findElement(By.name("eventName")).click();
    driver.findElement(By.name("eventName")).clear();
    driver.findElement(By.name("eventName")).sendKeys("CNY");
    driver.findElement(By.name("weekNo")).click();
    driver.findElement(By.name("weekNo")).clear();
    driver.findElement(By.name("weekNo")).sendKeys("5");
    driver.findElement(By.name("startTime")).click();
    driver.findElement(By.name("startTime")).clear();
    driver.findElement(By.name("startTime")).sendKeys("08:30");
    driver.findElement(By.name("endTime")).click();
    driver.findElement(By.name("endTime")).clear();
    
    driver.findElement(By.name("endTime")).sendKeys("19:00");
    driver.findElement(By.xpath("(.//*[normalize-space(text()) and normalize-space(.)='End Time'])[1]/following::input[2]")).click();
    
    Thread.sleep(2000);
    assertEquals ("constraints_View", driver.getTitle());
  }
  
  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

}
